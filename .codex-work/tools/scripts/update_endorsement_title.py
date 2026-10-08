from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil

import numpy as np
import pymupdf


ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "article" / "for-signature-final-defense-endorsement.pdf"
OLD_TITLE = "Physics Enforcement on Machine Learning Surrogates of the Activated Sludge Process"


def spans(page: pymupdf.Page) -> list[dict]:
    return [
        span
        for block in page.get_text("dict")["blocks"]
        if block["type"] == 0
        for line in block["lines"]
        for span in line["spans"]
        if span["text"].strip()
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--font-file", type=Path)
    arguments = parser.parse_args()
    manuscript = (ROOT / "article" / "manuscript.tex").read_text(encoding="utf-8")
    title_match = re.search(r"\\newcommand\{\\thesisTitle\}\{([^}]+)\}", manuscript)
    if title_match is None:
        raise ValueError("The current dissertation title was not found.")
    new_title = title_match.group(1)
    with pymupdf.open(PDF) as document:
        if len(document) != 1 or document.get_sigflags() > 0:
            raise ValueError("Expected the unsigned, single-page endorsement form.")
        page = document[0]
        original_spans = spans(page)
        title_spans = [span for span in original_spans if span["text"].strip() == OLD_TITLE]
        if len(title_spans) != 1:
            raise ValueError("The old title must occur in exactly one text span.")
        title_span = title_spans[0]
        if arguments.font_file is not None:
            font_buffer = arguments.font_file.read_bytes()
        else:
            resources = [
                resource for resource in page.get_fonts(full=True)
                if resource[3].split("+", 1)[-1] == title_span["font"]
            ]
            font_buffer = document.extract_font(resources[0][0])[3]
        font = pymupdf.Font(fontbuffer=font_buffer)
        missing_glyphs = sorted({character for character in new_title if not character.isspace() and not font.has_glyph(ord(character))})
        if missing_glyphs:
            raise ValueError(f"The embedded font lacks {missing_glyphs}; supply the full font with --font-file.")
        font_size = title_span["size"]
        words = new_title.split()
        splits = [(" ".join(words[:index]), " ".join(words[index:])) for index in range(1, len(words))]
        title_lines = min(splits, key=lambda lines: max(font.text_length(line, fontsize=font_size) for line in lines))
        left, baseline = title_span["origin"]
        right = page.rect.width - 72
        if max(font.text_length(line, fontsize=font_size) for line in title_lines) > right - left:
            raise ValueError("The two-line title exceeds the existing page margins.")
        line_spacing = font_size * 1.25
        replacement_area = pymupdf.Rect(left - 2, title_span["bbox"][1] - 2, right + 2, title_span["bbox"][3] + line_spacing + 2)
        outside_spans = [span for span in original_spans if span is not title_span]
        if any(replacement_area.intersects(pymupdf.Rect(span["bbox"])) for span in outside_spans):
            raise ValueError("The new title area overlaps other form text.")
        print(json.dumps({"title": new_title, "lines": title_lines, "font": font.name, "font_size": font_size, "area": list(replacement_area)}, indent=2), flush=True)
        if arguments.check:
            print("PASS: Title, font coverage, two-line fit, and separation from form text.", flush=True)
            return
        work = ROOT / ".codex-work" / "reviews" / (datetime.now().strftime("%Y-%m-%d-%H%M%S") + "-endorsement-title")
        work.mkdir()
        shutil.copy2(PDF, work / "original.pdf")
        before_pixels = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        before_pixels.save(work / "before.png")
        page.add_redact_annot(pymupdf.Rect(title_span["bbox"]), fill=(1, 1, 1))
        page.apply_redactions(images=0, graphics=0, text=0)
        page.insert_font(fontname="EndorsementTitle", fontbuffer=font_buffer)
        for index, line in enumerate(title_lines):
            page.insert_text((left, baseline + index * line_spacing), line, fontname="EndorsementTitle", fontsize=font_size, color=(0, 0, 0))
        document.set_metadata({**document.metadata, "title": new_title})
        candidate = work / "updated.pdf"
        document.save(candidate, garbage=4, deflate=True)
    with pymupdf.open(candidate) as updated:
        updated_page = updated[0]
        updated_spans = spans(updated_page)
        updated_text = " ".join(updated_page.get_text().split())
        if new_title not in updated_text or OLD_TITLE in updated_text:
            raise ValueError("The updated PDF does not contain the exact new title.")
        preserved_text = sorted(span["text"] for span in outside_spans)
        actual_text = sorted(span["text"] for span in updated_spans if " ".join(span["text"].split()) not in title_lines)
        if preserved_text != actual_text:
            raise ValueError("Non-title form text changed.")
        for span in updated_spans:
            if " ".join(span["text"].split()) in title_lines and not replacement_area.contains(pymupdf.Rect(span["bbox"])):
                raise ValueError("The rendered title extends outside its allotted area.")
        after_pixels = updated_page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        after_pixels.save(work / "after.png")
        original_image = np.frombuffer(before_pixels.samples, dtype=np.uint8).reshape(before_pixels.height, before_pixels.width, before_pixels.n)
        updated_image = np.frombuffer(after_pixels.samples, dtype=np.uint8).reshape(after_pixels.height, after_pixels.width, after_pixels.n)
        if original_image.shape != updated_image.shape:
            raise ValueError("The page dimensions changed.")
        changed_pixels = np.any(original_image != updated_image, axis=2)
        changed_pixels[int(replacement_area.y0 * 2):int(np.ceil(replacement_area.y1 * 2)), int(replacement_area.x0 * 2):int(np.ceil(replacement_area.x1 * 2))] = False
        if changed_pixels.any():
            raise ValueError("The rendered form changed outside the title area.")
        if updated.metadata["title"] != new_title:
            raise ValueError("The PDF title metadata was not updated.")
    os.replace(candidate, PDF)
    print(f"PASS: Updated {PDF}; all other form text and pixels preserved.", flush=True)
    print(f"Original backup and previews: {work}", flush=True)


if __name__ == "__main__":
    main()