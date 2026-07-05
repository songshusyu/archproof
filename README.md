# ArchProof

> Project: **ArchProof**. Installable skill: `archproof-audit`.

ArchProof is a Codex/Agent skill for auditing architecture claims against real repository and runtime evidence.

It is designed for backend, distributed, event-driven, real-time, and AI-enabled systems where a report or design document must be traceable to code, configuration, database constraints, Redis keys, MQ queues, automated tests, logs, and reproducible deployment evidence.

## Why this exists

Architecture reports often say “we use Redis, MQ, Gateway, WebSocket, and LLM”, but the hard question is:

> Which claim is proven by which service, endpoint, table, key, queue, test, and runtime artifact?

ArchProof turns that question into a repeatable workflow. It helps an agent produce:

- requirement-to-evidence traceability;
- defect findings with impact and fix direction;
- evidence passports for core flows;
- test and failure-injection plans;
- qualified conclusions that separate “implemented”, “tested”, “designed”, and “unsupported”.

## Repository layout

```text
skills/archproof-audit/
  SKILL.md
  agents/openai.yaml
  references/
    architecture-checklist.md
    course-project-profile.md
    evidence-passport.md
  scripts/
    collect_architecture_evidence.py
    test_collect_architecture_evidence.py
```

The installable skill is only `skills/archproof-audit/`. Repository-level files such as this README, license, CI, and contribution notes are for humans and maintainers.

## Install

Clone the repository and copy or symlink the skill folder into your Codex skills directory:

```powershell
git clone git@github.com:songshusyu/archproof.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\archproof\skills\archproof-audit" "$env:USERPROFILE\.codex\skills\archproof-audit"
```

Or keep the skill in a project-local agent directory if your agent runtime supports project skills:

```text
.agents/skills/archproof-audit/
```

## Validate

If you have the Codex skill creator validator installed, run:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  skills\archproof-audit
```

Portable checks that do not depend on a local Codex installation:

```powershell
python -m py_compile skills\archproof-audit\scripts\collect_architecture_evidence.py
python -m py_compile skills\archproof-audit\scripts\test_collect_architecture_evidence.py
python skills\archproof-audit\scripts\test_collect_architecture_evidence.py
```

The scanner can be smoke-tested on any backend repository:

```powershell
python skills\archproof-audit\scripts\collect_architecture_evidence.py `
  --root path\to\your\repo `
  --output tmp\archproof-evidence.json `
  --exclude target --exclude node_modules
```

## Example use

Ask your agent:

> Use ArchProof to audit whether this project’s architecture report is supported by code, Redis/MQ configuration, database constraints, tests, and runtime evidence. Produce a traceability matrix and prioritized defects.

ArchProof does not try to prove architecture by dependency names alone. It asks whether business invariants, failure paths, identity boundaries, and reproducibility claims are backed by evidence.

See [examples/](examples/) for a small sample scanner output.

## Scope

Good fit:

- microservice and gateway projects;
- Redis/MQ consistency and idempotency checks;
- WebSocket/SSE real-time flows;
- AI/LLM governance and fallback claims;
- course projects and production-readiness reviews;
- performance and failure-recovery evidence audits.

Out of scope:

- replacing full security penetration testing;
- inventing missing benchmark numbers;
- asserting production readiness without runtime evidence;
- claiming originality for standard patterns such as Outbox, Lua atomicity, or queue-based scaling.

## License

Apache License 2.0. See [LICENSE](LICENSE).
