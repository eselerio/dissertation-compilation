# 2026-10-09-workspace-organization

Migration record and documentation for the 2026-10-09 reorganization.

[Parent guide](../README.md) | [Workspace guide](../../README.md)

## Contents

- [apply_layout.ps1](apply_layout.ps1)
- [migration.json](migration.json)
- [organize_workspace.py](organize_workspace.py)
- [validation.json](validation.json) — file-preservation and navigation checks.

These artifacts are historical evidence. Check `article/` for maintained manuscript sources.

## What changed

The migration moved 118 top-level entries containing 774 files into purpose
categories. It normalized folder names and ordinary artifact names, retained
Python module names and snapshot source names, updated executable paths, and
replaced obsolete absolute paths in standalone wrappers with repository-root
relative inputs. The Windows virtual environment stayed in place.

`migration.json` maps every original file to its destination and records its
original SHA-256 hash. Its `updated_files` list identifies the 51 artifacts
whose script, Markdown, or wrapper paths were revised. All other 723 migrated
files were checked against their original hashes.

The migration scripts are a record of this one-time operation. Do not rerun
them on the organized workspace. Maintain documentation directly and use the
[read-only validator](../../tools/maintenance/validate_workspace.py) for future
layout checks.

## Validation

All original artifacts were found at their destinations, with no unexpected
content changes. Managed folders have READMEs, documentation links resolve,
and Python scripts parse without execution. Maintained `article/` files were
unchanged. This operation did not rebuild historical PDFs or replay manuscript
editing scripts.
