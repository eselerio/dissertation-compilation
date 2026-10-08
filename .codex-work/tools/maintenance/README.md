# maintenance

Read-only workspace navigation and integrity checks.

[Parent guide](../README.md) | [Workspace guide](../../README.md)

## Contents

- [validate_workspace.py](validate_workspace.py) — read-only README, local-link,
  Python syntax, repository-root, artifact-path, and sibling-import checks.

Run from the repository root:

```powershell
python .codex-work/tools/maintenance/validate_workspace.py
```

The check does not execute historical manuscript editing scripts or load
third-party environment packages. It exits with status 1 when a check fails.
