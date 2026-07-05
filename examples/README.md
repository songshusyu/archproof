# Examples

This directory contains small, non-private examples that show the expected shape of ArchProof outputs.

Run the scanner against a repository:

```powershell
python ..\skills\archproof-audit\scripts\collect_architecture_evidence.py `
  --root path\to\your\repo `
  --format markdown `
  --output examples\evidence-candidates.sample.md `
  --exclude target `
  --exclude node_modules
```

The scanner output is not a completion certificate. It only lists candidate files and lines that an agent or reviewer should inspect before assigning implementation status.
