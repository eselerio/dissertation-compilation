# Working in .codex-work

Read [README.md](README.md) first, then the destination folder README. Use
[ARTIFACT_INDEX.md](ARTIFACT_INDEX.md) to resolve previous artifact paths.

Keep new artifacts in the documented purpose categories and add a README to
each managed folder. Preserve historical evidence and original snapshot names.
Keep dated review runs together. Installed environment internals and generated
`__pycache__` directories are exempt from README coverage.

Run utilities from the repository root. Inspect historical editing scripts
before executing or importing them: many immediately modify `article/`.

After layout changes, run the read-only navigation check:

```powershell
python .codex-work/tools/maintenance/validate_workspace.py
```
