# Contributing

Thanks for improving ArchProof.

## Principles

- Keep the installable skill concise.
- Put detailed checklists in `references/`, not in `SKILL.md`.
- Prefer deterministic scripts for repeatable evidence collection.
- Do not add project-specific secrets, logs, reports, or private datasets.
- Never invent benchmark or production results.

## Local checks

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  skills\archproof-audit

python -m py_compile skills\archproof-audit\scripts\collect_architecture_evidence.py
python -m py_compile skills\archproof-audit\scripts\test_collect_architecture_evidence.py
python skills\archproof-audit\scripts\test_collect_architecture_evidence.py
```

## Pull request checklist

- [ ] `SKILL.md` frontmatter still has only `name` and `description`.
- [ ] New guidance is generic or isolated behind a clearly named reference file.
- [ ] Scripts have tests or a documented smoke test.
- [ ] No API keys, tokens, passwords, private URLs, or course/project-only artifacts are committed.
