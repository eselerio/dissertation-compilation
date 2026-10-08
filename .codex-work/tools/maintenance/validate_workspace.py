"""Read-only checks for workspace documentation and path integrity."""
from pathlib import Path
import ast
import json
import os
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / '.codex-work'


def main():
    errors = []
    directories = []
    files = []
    for parent, children, names in os.walk(WORK):
        children[:] = sorted(name for name in children if name != '__pycache__')
        directory = Path(parent)
        directories.append(directory)
        if directory == WORK / 'visual-env':
            children[:] = []
            names = ['README.md']
        files.extend(directory / name for name in names)
        if not (directory / 'README.md').is_file():
            errors.append(f'Missing README: {directory.relative_to(WORK)}')
    checked_links = 0
    for path in files:
        if path.suffix != '.md':
            continue
        for raw in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = raw.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            checked_links += 1
            if not (path.parent / unquote(target)).exists():
                errors.append(f'Broken link in {path.relative_to(WORK)}: {raw}')
    parsed = 0
    script_paths = 0
    for path in files:
        if path.suffix != '.py':
            continue
        text = path.read_text(encoding='utf-8-sig')
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as error:
            errors.append(str(error))
            continue
        parsed += 1
        for match in re.finditer(r'Path\(__file__\)\.resolve\(\)\.parents\[(\d+)\]', text):
            if path.parents[int(match[1])] != ROOT:
                errors.append(f'Wrong repository root in {path.relative_to(WORK)}')
        # Migration utility intentionally records old names; it is not a current consumer.
        if path.name == 'organize_workspace.py':
            continue
        for match in re.finditer(r"['\"](\.codex-work/[^'\"\n]+)['\"]", text):
            target = match[1]
            if '*' in target or target.endswith('/'):
                continue
            script_paths += 1
            if not (ROOT / target).exists():
                errors.append(f'Missing script artifact in {path.relative_to(WORK)}: {target}')
        for match in re.finditer(r"\bWORK\s*/\s*['\"]([^'\"\n]+)['\"]", text):
            script_paths += 1
            if not (WORK / match[1]).exists():
                errors.append(f'Missing WORK artifact in {path.relative_to(WORK)}: {match[1]}')
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in {'audit', 'build_bibliography'}:
                if not (path.parent / (node.module + '.py')).is_file():
                    errors.append(f'Missing sibling import {node.module} in {path.relative_to(WORK)}')
    print(json.dumps({'managed_directories': len(directories), 'checked_links': checked_links,
        'parsed_python_scripts': parsed, 'checked_script_artifact_paths': script_paths,
        'errors': errors}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
