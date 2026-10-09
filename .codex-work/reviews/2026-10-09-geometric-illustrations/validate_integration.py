"""Read-only source preservation and new figure reference checks."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = {}
    figures = []
    blocks = r"\\begin\{(equation\*?|align\*?|gather\*?)\}.*?\\end\{\1\}"
    for previous in sorted((REVIEW / "before").glob("*.tex")):
        current = ROOT / "article/chapters" / previous.name
        old, new = previous.read_text(encoding="utf-8"), current.read_text(encoding="utf-8")
        eq_before = [m.group() for m in re.finditer(blocks, old, re.S)]
        eq_after = [m.group() for m in re.finditer(blocks, new, re.S)]
        checks[previous.name] = {"existing_display_equations_unchanged": eq_before == eq_after,
                                 "display_equations": len(eq_before)}
        # Preserve all original paragraphs in order, including experimental results.
        previous_paragraphs = [p for p in re.split(r"\n\s*\n", old) if p.strip()]
        pos = 0
        for paragraph in previous_paragraphs:
            found = new.find(paragraph, pos)
            if found == -1:
                raise AssertionError(f"Original text changed or removed in {previous.name}: {paragraph[:120]}")
            pos = found + len(paragraph)
        checks[previous.name]["all_original_text_preserved_in_order"] = True
        for asset in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*geometry[^}]*)\}", new):
            full = ROOT / "article" / asset
            if not full.is_file():
                full = ROOT / "article/figures" / asset
            assert full.is_file(), asset
            assert full.suffix == ".png", asset
            assert full.with_suffix(".pdf").is_file(), asset
            figures.append({"chapter": previous.name, "asset": str(full.relative_to(ROOT)), "sha256": sha(full)})
    source = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "article/chapters").glob("*.tex"))
    labels = re.findall(r"\\label\{([^}]+)\}", source)
    assert len(labels) == len(set(labels)), "Duplicate chapter labels"
    references = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", source)
    # A few labels may be defined in the front matter/main manuscript.
    main_source = (ROOT / "article/manuscript.tex").read_text(encoding="utf-8")
    all_labels = set(labels + re.findall(r"\\label\{([^}]+)\}", main_source))
    unresolved = sorted(set(references)-all_labels)
    checks["unique_chapter_labels"] = True
    checks["unresolved_references_static"] = unresolved
    checks["new_geometric_figures"] = figures
    checks["new_geometric_figure_count"] = len(figures)
    assert len(figures) == 8, len(figures)
    assert all(v["existing_display_equations_unchanged"] for v in checks.values() if isinstance(v, dict))
    checks["preservation_checks_pass"] = True
    (REVIEW / "integration-validation.json").write_text(json.dumps(checks, indent=2)+"\n", encoding="utf-8")
    print(f"Original text and displayed equations preserved; {len(figures)} PNG figures resolve.")
    if unresolved:
        print("Static references requiring build confirmation:", unresolved)


if __name__ == "__main__":
    main()
