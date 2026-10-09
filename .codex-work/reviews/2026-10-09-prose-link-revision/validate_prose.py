"""Check protected dissertation content and prose punctuation after style edits."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent


def protected(source):
    pattern = (r"\\begin\{(equation\*?|align\*?|gather\*?|tikzpicture)\}.*?\\end\{\1\}"
               r"|\\\(.*?\\\)|\\\[.*?\\\]|\$.*?\$"
               r"|\\(?:citep|citet|cite|label|ref|eqref|url|includegraphics|input)"
               r"(?:\[[^\]]*\])?\{[^}]*\}")
    return [m.group() for m in re.finditer(pattern, source, re.S)]


def main():
    files, remaining = [], []
    for before_path in sorted((REVIEW / "before").glob("*.tex")):
        current = ROOT / "article/manuscript.tex" if before_path.name == "manuscript.tex" else ROOT / "article/chapters" / before_path.name
        before, after = before_path.read_text(encoding="utf-8"), current.read_text(encoding="utf-8")
        assert protected(before) == protected(after), f"Protected content changed: {before_path.name}"
        before_numbers = re.findall(r"\d+(?:\.\d+)?", before)
        after_numbers = re.findall(r"\d+(?:\.\d+)?", after)
        assert before_numbers == after_numbers, f"Numerical sequence changed: {before_path.name}"
        # Tables, equations and diagrams are preserved in addition to all inline mathematics.
        tables = r"\\begin\{(tabular\*?|tabularx|longtable)\}.*?\\end\{\1\}"
        assert [m.group() for m in re.finditer(tables, before, re.S)] == [m.group() for m in re.finditer(tables, after, re.S)]
        skip = False
        for i, line in enumerate(after.splitlines(), 1):
            if re.search(r"\\begin\{(?:equation\*?|align\*?|tikzpicture|gather\*?)\}", line):
                skip = True
            if skip:
                if re.search(r"\\end\{(?:equation\*?|align\*?|tikzpicture|gather\*?)\}", line):
                    skip = False
                continue
            if line.lstrip().startswith("%"):
                continue
            masked = re.sub(r"\\\(.*?\\\)|\$.*?\$|\\(?:label|ref|eqref|url|citep|citet|cite)\{[^}]*\}", " ", line)
            if re.search(r":|;|---|\u2014", masked):
                assert re.search(r"doi:\s+10\.", masked), (before_path.name, i, line)
                remaining.append({"file": before_path.name, "line": i, "reason": "DOI identifier convention"})
        files.append({"file": before_path.name, "changed": before != after,
                      "protected_math_citations_labels_inputs_preserved": True,
                      "all_numeric_tokens_preserved_in_order": True,
                      "table_content_preserved": True})
    record = {"files": files, "remaining_prose_punctuation": remaining,
              "explanatory_colons_and_semicolon_links_remaining": 0, "all_checks_pass": True}
    (REVIEW / "validation.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    print("Validation passed: protected content and numerical tokens preserved; no explanatory colon or semicolon links remain.")


if __name__ == "__main__":
    main()
