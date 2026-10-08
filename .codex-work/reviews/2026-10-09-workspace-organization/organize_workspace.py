"""Record and document the 2026-10-09 workspace migration; not a routine runner."""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / '.codex-work'
OUT = Path(__file__).resolve().parent
PLAN = OUT / 'migration.json'

GROUPS = {
    'snapshots/original-manuscript': ['original'],
    'snapshots/before-math-expansion': ['before_math_expansion'],
    'snapshots/before-proposal-integration': ['before_proposal_integration'],
    'snapshots/ch02-before-import': ['chapter2_import_backup'],
    'previews/ch05-diagrams': ['ch5_figures'],
    'previews/ch06-diagrams': ['ch6_fig_preview'],
    'previews/concept-diagrams': ['concept-proof'],
    'previews/reactor-diagrams': ['reactor-diagram-proof'],
    'previews/results': ['result-proof'],
    'builds/manuscript': ['pdf_build'],
    'builds/mathematics': ['math-proof'],
    'references/crossref-cache': ['crossref'],
    'runtime/python-cache': ['__pycache__'],
}
REVIEW_NAMES = {
    'chapter-restructure-20261008': '2026-10-08-chapter-restructure',
    'chapter1-style-revision': 'ch01-style-revision',
    'chapter2-literature-review': 'ch02-literature-review',
    'citation-strengthening-20261008': '2026-10-08-citation-strengthening',
    'editorial-review': 'manuscript-editorial-review',
    'endorsement-title-20261008_090436': '2026-10-08-090436-endorsement-title',
    'endorsement-title-20261008_090655': '2026-10-08-090655-endorsement-title',
    'introduction-citation-review': 'ch01-citation-review',
    'rationale-practical-synthesis-20261008': '2026-10-08-rationale-practical-synthesis',
    'reference-audit-20261009': '2026-10-09-reference-audit',
}
FILES = {
    'sources/proposal': ['approved-proposal-layout.txt', 'approved-proposal.txt',
        'proposal-formulation.txt', 'proposal-intro.txt', 'proposal-purpose.txt',
        'proposal-references.txt', 'proposal-theory.txt'],
    'sources/components': ['icsor-layout.txt', 'icsor.txt', 'icsor_editorial_source.txt',
        'projection-supplement.txt'],
    'sources/manuscript-text': ['dissertation-layout.txt', 'final-dissertation-layout.txt',
        'review-current-pdf.txt'],
    'references/records': ['bibliography_records.json', 'citation_aliases.json',
        'final_reference_metadata.json', 'icsor_references.json',
        'proposal_reference_decisions.json', 'proposal_reference_inventory.json',
        'proposal_selected_reference_keys.json'],
    'references/imports': ['manual_references.bib', 'proposal_manual_references.bib',
        'proposal_reference_import.bib', 'references_import.bib'],
    'references/inventories': ['icsor_reference_inventory.md',
        'optimization_reference_inventory.md', 'projection_reference_inventory.md'],
    'references/notes': ['icsor_literature_notes.md', 'optimization_literature_notes.md',
        'icsor_review_audit.md'],
    'reports/manuscript': ['completion_report.json', 'manuscript_audit.json',
        'math_and_visual_completion.json', 'terminology_pass.json', 'integration_review.md'],
    'reports/mathematics': ['math_expansion_03_04.md', 'math_expansion_05.md',
        'math_expansion_06.md', 'math_expansion_05_validation.json',
        'math_expansion_audit.json', 'plant_method_expansions.json'],
    'reports/figures': ['ch5_concept_visuals.md', 'ch6_concept_figures.md',
        'concept_diagram_exports.json', 'independent_figure_review.md',
        'visual_expansion_03_04.md'],
    'reports/proposal-import': ['chapter2_import_report.json'],
    'builds/logs': ['build.log', 'build_math_expansion.log', 'build_visuals.log',
        'chapter2_import_build.log'],
    'builds/ch05-mathematics': ['math05_check.aux', 'math05_check.log',
        'math05_check.pdf', 'math05_check.tex'],
    'previews/component-figures': ['comparator-preview.png', 'component-preview.png',
        'plant-preview.png', 'search-domain-preview.png'],
    'previews/manuscript-pages': ['final-page-100.png', 'final-page-105.png',
        'final-page-174.png', 'final-page-23.png'],
    'drafts/introduction': ['new_introduction.tex'],
}
PURPOSES = {
    '.': 'Agent working artifacts for the dissertation. Start here before searching or creating working files.',
    'sources': 'Extracted text used as input to manuscript and literature work.',
    'sources/proposal': 'Approved proposal extracts, including individual section extracts and layout-preserving text.',
    'sources/components': 'ICSOR component article extracts and projection supplementary text.',
    'sources/manuscript-text': 'Historical text extractions of dissertation PDFs. Pagination and text reflect the extraction run.',
    'snapshots': 'Preserved manuscript baselines for comparison and recovery. Keep original source filenames inside each snapshot.',
    'snapshots/original-manuscript': 'Initial manuscript, bibliography, and PDF used during assembly.',
    'snapshots/before-math-expansion': 'Manuscript baseline before mathematical expansions.',
    'snapshots/before-proposal-integration': 'Manuscript baseline before approved-proposal integration.',
    'snapshots/ch02-before-import': 'Chapter 2, manuscript entry point, and bibliography before the chapter import.',
    'references': 'Historical bibliography imports, records, inventories, notes, and shared Crossref responses.',
    'references/crossref-cache': 'DOI-named Crossref response JSON from bibliography construction. Preserve DOI-derived filenames.',
    'references/records': 'Bibliography metadata, citation aliases, and proposal-reference import decisions.',
    'references/imports': 'Intermediate and manually completed BibTeX import collections.',
    'references/inventories': 'Reference inventories by component study: ICSOR, optimization, and projection.',
    'references/notes': 'Literature synthesis notes and ICSOR review evidence.',
    'reports': 'Cross-task summaries and validation outputs. Individual review runs retain their own reports under reviews/.',
    'reports/manuscript': 'Manuscript assembly, completion, terminology, integration, and citation audit reports.',
    'reports/mathematics': 'Chapter mathematical expansion reports, validation records, and chapter 6 insertion data.',
    'reports/figures': 'Concept-figure design, export, and independent review reports.',
    'reports/proposal-import': 'Chapter 2 approved-proposal import report.',
    'reviews': 'Task-specific review records. Each run keeps its scripts, reports, before-files, logs, and previews together.',
    'reviews/2026-10-09-workspace-organization': 'Migration record and documentation for the 2026-10-09 reorganization.',
    'builds': 'Historical compilation artifacts and diagnostic logs. New manuscript builds use the repository PDF build workflow.',
    'builds/manuscript': 'Historical full-manuscript build output and page previews.',
    'builds/mathematics': 'Historical mathematical-expansion LaTeX auxiliary output.',
    'builds/ch05-mathematics': 'Chapter 5 standalone mathematics wrapper, PDF, and compilation diagnostics.',
    'builds/logs': 'Top-level historical manuscript, mathematical, visual, and proposal-import build logs.',
    'previews': 'Rendered images and standalone concept-diagram wrappers for visual inspection.',
    'previews/ch05-diagrams': 'Chapter 5 training, prediction, and deployment standalone diagram exports.',
    'previews/ch06-diagrams': 'Chapter 6 projection and verification flowchart previews.',
    'previews/concept-diagrams': 'Standalone concept diagram exports spanning the manuscript chapters.',
    'previews/reactor-diagrams': 'Reactor accounting and projection diagram proofs, with an independent chapter 1 proof.',
    'previews/results': 'Chapter 4-6 quantitative result previews and historical verification evidence.',
    'previews/component-figures': 'Individual component, plant, comparator, and search-domain figure previews.',
    'previews/manuscript-pages': 'Historical final-dissertation page screenshots; page numbers belong to that build.',
    'drafts': 'Working manuscript fragments that are separate from the maintained article sources.',
    'drafts/introduction': 'Historical replacement introduction draft.',
    'tools': 'Workspace utilities and historical manuscript transformation scripts.',
    'tools/scripts': 'Existing Python and PowerShell utilities. Python filenames and a shared directory preserve sibling imports.',
    'tools/maintenance': 'Read-only workspace navigation and integrity checks.',
    'runtime': 'Local disposable execution artifacts. This directory is excluded from Git.',
    'runtime/python-cache': 'Relocated original Python bytecode cache; not a source or a validation record.',
    'visual-env': 'Existing local Python environment for plotting and PDF inspection. Kept at its original path for Windows launcher compatibility.',
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    if PLAN.exists():
        raise SystemExit('Migration already recorded. Do not rerun preparation.')
    mapping = {}
    for destination, names in GROUPS.items():
        for name in names:
            mapping[name] = destination
    mapping.update({name: 'reviews/' + new for name, new in REVIEW_NAMES.items()})
    for destination, names in FILES.items():
        for name in names:
            mapping[name] = destination + '/' + name.replace('_', '-')
    for path in WORK.iterdir():
        if path.is_file() and path.suffix in {'.py', '.ps1'}:
            mapping[path.name] = 'tools/scripts/' + path.name
    candidates = {p.name for p in WORK.iterdir()} - {'reviews', 'visual-env'}
    assert candidates == set(mapping), (candidates - set(mapping), set(mapping) - candidates)
    assert len(set(mapping.values())) == len(mapping)
    records = []
    for old, new in sorted(mapping.items()):
        source = WORK / old
        paths = sorted(p for p in source.rglob('*') if p.is_file()) if source.is_dir() else [source]
        for path in paths:
            suffix = path.relative_to(source).as_posix() if source.is_dir() else ''
            records.append({'old': path.relative_to(WORK).as_posix(),
                'new': new + ('/' + suffix if suffix else ''), 'sha256': digest(path)})
    plan = {'date': '2026-10-09', 'mapping': mapping, 'files': records,
        'environment_preserved': 'visual-env', 'updated_files': []}
    PLAN.write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print(f'Recorded {len(mapping)} moves and {len(records)} original file hashes.')

def rewrite_paths(plan):
    mapping = plan['mapping']
    changed = []
    for record in plan['files']:
        path = WORK / record['new']
        # Preserve original evidence, metadata, compiled output, and snapshot bytes.
        if path.suffix not in {'.py', '.ps1', '.md'}:
            continue
        if record['new'].startswith('snapshots/') or '/original/' in record['new']:
            continue
        data = path.read_bytes()
        text = data.decode('utf-8-sig')
        before = text
        for old, new in sorted(mapping.items(), key=lambda item: -len(item[0])):
            text = text.replace('.codex-work/' + old, '.codex-work/' + new)
            # Shared WORK is the .codex-work directory in bibliography utilities.
            text = re.sub(r"(\bWORK\s*/\s*)(['\"])" + re.escape(old) + r"(?=/|['\"])",
                lambda m: m[1] + m[2] + new, text)
        if path.suffix == '.py':
            depth = len(path.relative_to(ROOT).parts) - 1
            text = re.sub(r'Path\(__file__\)\.resolve\(\)\.parents\[\d+\]',
                f'Path(__file__).resolve().parents[{depth}]', text)
            text = text.replace('ROOT / ".codex-work" / "audit_manuscript.py"',
                'ROOT / ".codex-work" / "tools/scripts/audit_manuscript.py"')
            text = text.replace('ROOT / ".codex-work" / "result-proof"',
                'ROOT / ".codex-work" / "previews/results"')
            text = text.replace("Path(__file__).with_name('plant_method_expansions.json')",
                "(Path(__file__).resolve().parents[3] / '.codex-work/reports/mathematics/plant-method-expansions.json')")
            text = text.replace('ROOT / ".codex-work" / ("endorsement-title-" + datetime.now().strftime("%Y%m%d_%H%M%S"))',
                'ROOT / ".codex-work" / "reviews" / (datetime.now().strftime("%Y-%m-%d-%H%M%S") + "-endorsement-title")')
            text = text.replace('        work.mkdir()\n', '        work.mkdir(parents=True)\n'
                '        (work / "README.md").write_text("# Endorsement title review\\n\\nOriginal and updated endorsement forms with before/after previews.\\n", encoding="utf-8")\n')
        if path.name == 'label_equations.ps1':
            text = text.replace('Split-Path $PSScriptRoot -Parent',
                'Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent')
        if text != before:
            # Preserve original line ending convention.
            newline = '\r\n' if b'\r\n' in data else '\n'
            path.write_bytes(text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8'))
            changed.append(record['new'])
    # Make historical standalone wrappers use repository-root relative inputs.
    wrappers = list((WORK / 'previews').rglob('*.tex')) + list((WORK / 'builds/ch05-mathematics').glob('*.tex'))
    for path in wrappers:
        before = path.read_text(encoding='utf-8')
        text = re.sub(r'C:/Users/eggy/Repos/deng-dissertation-manuscript/article/', 'article/', before)
        if text != before:
            path.write_text(text, encoding='utf-8')
            changed.append(path.relative_to(WORK).as_posix())
    plan['updated_files'] = sorted(changed)
    PLAN.write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')

def directories():
    yield WORK
    for parent, dirs, files in __import__('os').walk(WORK):
        dirs[:] = sorted(d for d in dirs if d != '__pycache__')
        base = Path(parent)
        if base == WORK / 'visual-env':
            dirs[:] = []
        for directory in dirs:
            yield base / directory

def document(plan):
    (WORK / 'tools/maintenance').mkdir(parents=True, exist_ok=True)
    for path in directories():
        key = path.relative_to(WORK).as_posix()
        purpose = PURPOSES.get(key)
        if not purpose:
            if key.startswith('reviews/'):
                purpose = 'Preserved task evidence for ' + key.split('/')[1] + '.'
                if '/original' in key:
                    purpose += ' These are baseline copies; keep their source filenames and contents.'
                elif key.endswith('/crossref'):
                    purpose += ' Citation-keyed Crossref lookup records; separate from the shared DOI cache.'
                elif key.endswith('/external'):
                    purpose += ' Retrieved external metadata and source files used in this review.'
            elif key.startswith('snapshots/'):
                purpose = 'Preserved baseline ' + path.name + ' files from the parent snapshot. Keep original contents and filenames.'
            else:
                purpose = 'Working artifacts belonging to the parent category.'
        readme = path / 'README.md'
        title = '.codex-work' if path == WORK else path.name
        lines = ['# ' + title, '', purpose, '']
        if path != WORK:
            lines += ['[Parent guide](../README.md) | [Workspace guide](' +
                '/'.join(['..'] * len(path.relative_to(WORK).parts)) + '/README.md)', '']
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        if key == 'visual-env':
            lines += ['Use `./.codex-work/visual-env/Scripts/python.exe` from the repository root.', '',
                'This environment is ignored by Git. Recreate it if needed; do not relocate its installed launchers.', '',
                'Its third-party `Lib/`, `Scripts/`, and package internals are exempt from workspace README requirements.', '']
        else:
            items = [p for p in entries if p.name not in {'README.md', '__pycache__'}]
            lines += ['## Contents', '']
            for item in items:
                destination = item.name + ('/README.md' if item.is_dir() else '')
                lines.append(f'- [{item.name}{"/" if item.is_dir() else ""}]({destination})')
            if not items:
                lines.append('Add artifacts for this category here and describe them in this README.')
            lines.append('')
        if key.startswith(('snapshots', 'sources', 'reviews')):
            lines += ['These artifacts are historical evidence. Check `article/` for maintained manuscript sources.', '']
        if key.startswith(('builds', 'previews')):
            lines += ['Outputs describe their original run and are not proof of the current manuscript state.', '',
                'Run standalone wrappers from the repository root so `article/` input paths resolve.', '']
        if key == 'references':
            lines += ['The maintained bibliography is `article/references.bib`. Imports and cached metadata here record earlier work.', '']
        readme.write_text('\n'.join(lines), encoding='utf-8')
    root_readme = WORK / 'README.md'
    root_readme.write_text(root_readme.read_text(encoding='utf-8') + MAINTENANCE, encoding='utf-8')
    rows = ['# Artifact path index', '', 'Paths are relative to `.codex-work/`. Directory mappings apply to all descendants.', '',
        '| Previous path | Current path |', '| --- | --- |']
    for old, new in sorted(plan['mapping'].items()):
        target = WORK / new
        link = new + ('/README.md' if target.is_dir() else '')
        rows.append(f'| `{old}` | [{new}]({link}) |')
    (WORK / 'ARTIFACT_INDEX.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')

MAINTENANCE = '''
## Where to start

| Need | Start here |
| --- | --- |
| Understand a specific revision or audit | [reviews](reviews/README.md) |
| Compare with an earlier manuscript | [snapshots](snapshots/README.md) |
| Find proposal or component text extracts | [sources](sources/README.md) |
| Find bibliography decisions or metadata | [references](references/README.md) |
| Find mathematical or figure validation | [reports](reports/README.md) |
| Inspect a figure or page | [previews](previews/README.md) |
| Inspect historical build diagnostics | [builds](builds/README.md) |
| Find a utility | [tools/scripts](tools/scripts/README.md) |
| Locate an artifact using its old name | [Artifact path index](ARTIFACT_INDEX.md) |

## Maintenance rules for Codex

1. Read this guide and the destination folder README before creating artifacts.
2. Keep maintained dissertation sources in `article/`. This workspace contains working material and historical evidence.
3. Choose the category by purpose. Keep a review run together under `reviews/YYYY-MM-DD-topic/`; add `-HHMMSS` when multiple runs need distinct names. Do not infer missing dates for older undated runs.
4. Use lowercase hyphenated names for new folders and ordinary artifacts. Keep Python module names in `snake_case`; retain source chapter filenames, citation keys, DOI cache names, and related LaTeX wrapper/output basenames.
5. Add a README to every managed folder and subfolder. State purpose, inputs, outputs, how to reproduce it when known, and which source files are maintained. Link to child READMEs and useful reports. Installed environment internals and generated `__pycache__` directories are exempt.
6. Preserve original snapshots, imported text, metadata responses, and historical logs. Record a new run instead of overwriting review evidence. Historical absolute paths inside logs and JSON describe the original run and can be resolved through the path index.
7. Run Python and PowerShell utilities from the repository root. Many older utilities immediately modify `article/` when run or imported. Read their code and the script guide before execution; do not replay historical edits just to test navigation.
8. When moving an artifact, update executable paths and current Markdown links, then add its mapping to `ARTIFACT_INDEX.md`. Keep related `.tex`, `.pdf`, `.png`, `.aux`, and `.log` basenames together.
9. Use `.codex/skills/build-latex-pdf/scripts/build_latex_pdf.ps1` for new manuscript PDF builds; its archives belong under `docs/latex_pdfs/`. The `builds/` records here are historical.
10. Keep local environments and runtime caches ignored by Git. Leave `visual-env/` at its existing path; recreate rather than move a Windows virtual environment.
11. Run `python .codex-work/tools/maintenance/validate_workspace.py` after changing the layout. The check reads files, validates README coverage and local links, and parses scripts without executing them.

## Reorganization record

The 2026-10-09 migration preserves every original artifact. Directory and ordinary artifact names were normalized, executable paths were updated, and standalone wrapper inputs now resolve from the repository root. Snapshot source names, Python module names, and evidence metadata were preserved.

[Migration record](reviews/2026-10-09-workspace-organization/README.md) contains the complete file mapping and SHA-256 hashes. The local virtual environment was kept in place. Reports and PDFs retain their original run dates and are not newly validated manuscript builds.
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['prepare', 'finish'])
    args = parser.parse_args()
    if args.phase == 'prepare':
        prepare()
    else:
        plan = json.loads(PLAN.read_text(encoding='utf-8'))
        if plan['updated_files']:
            raise SystemExit('Migration already finished. Maintain READMEs directly.')
        assert all((WORK / r['new']).is_file() for r in plan['files'])
        rewrite_paths(plan)
        document(plan)
        print(f'Updated {len(plan["updated_files"])} path-dependent artifacts and documented the layout.')
