#!/usr/bin/env python3
"""Collect architecture evidence candidates without claiming implementation completeness."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


CATEGORIES = {
    "gateway-security": [
        r"GatewayFilter", r"X-User-", r"Authorization", r"jwt", r"blacklist",
        r"/internal/", r"middleware", r"before_request",
    ],
    "cache-concurrency": [
        r"RedisScript", r"EVALSHA", r"\.lua\b", r"ZSET", r"ZINCRBY", r"SETNX",
        r"RequestRateLimiter", r"token.?bucket", r"sliding.?window", r"distributed.?lock",
    ],
    "messaging-reliability": [
        r"RabbitTemplate", r"KafkaTemplate", r"PublisherConfirm", r"basicAck", r"basicNack",
        r"dead.?letter", r"outbox", r"idempoten", r"consumer.?group", r"redeliver",
    ],
    "database-consistency": [
        r"@Transactional", r"BEGIN\b", r"COMMIT\b", r"ROLLBACK\b", r"UNIQUE",
        r"unique index", r"Flyway", r"Liquibase", r"migration",
    ],
    "realtime": [r"WebSocket", r"text/event-stream", r"ServerSentEvent", r"EventSource", r"Flux<"],
    "llm-governance": [
        r"DeepSeek", r"OpenAI", r"chat/completions", r"tool_call", r"embedding",
        r"prompt", r"semantic.?cache", r"rate.?limit", r"timeout",
    ],
    "api-contracts": [r"springdoc", r"OpenAPI", r"Swagger", r"api-docs", r"FastAPI\(", r"swagger-ui"],
    "deployment": [
        r"docker compose", r"docker-compose", r"healthcheck", r"depends_on",
        r"kind:\s*Deployment", r"kind:\s*Service", r"HorizontalPodAutoscaler", r"ScaledObject",
    ],
    "observability": [r"Micrometer", r"Prometheus", r"Grafana", r"OpenTelemetry", r"traceparent", r"SLO\b"],
    "tests-evidence": [r"newman", r"k6", r"pytest", r"junit", r"p\(95\)", r"p95", r"assertion", r"reconcil"],
}

TEXT_SUFFIXES = {
    ".java", ".kt", ".xml", ".yml", ".yaml", ".properties", ".sql", ".lua",
    ".json", ".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".cs", ".rb", ".php",
    ".rs", ".gradle", ".kts", ".ps1", ".sh", ".md", ".typ", ".toml", ".conf",
}
SKIP_DIRS = {
    ".git", "node_modules", "target", "dist", "build", ".idea", ".gradle", "output", "tmp",
    "data", "logs", "volumes", "vendor", ".venv", "venv", "__pycache__", ".pytest_cache",
}


def is_excluded(relative: Path, excludes: tuple[str, ...]) -> bool:
    normalized = relative.as_posix()
    return any(normalized == item or normalized.startswith(item.rstrip("/") + "/") for item in excludes)


def classify_path(relative: Path) -> str:
    parts = {part.lower() for part in relative.parts}
    name = relative.name.lower()
    if "test" in parts or "tests" in parts or "spec" in parts or "__tests__" in parts or name.startswith("test_"):
        return "test"
    if any(part in parts for part in {"deploy", "deployment", "k8s", "helm", "infra"}) or name.startswith("dockerfile"):
        return "deployment"
    if "docs" in parts or relative.suffix.lower() in {".md", ".typ"}:
        return "documentation"
    if "evidence" in parts or "reports" in parts:
        return "runtime-evidence"
    return "implementation"


def iter_files(root: Path, excludes: tuple[str, ...]):
    def ignore_walk_error(_: OSError) -> None:
        return None

    for directory, names, files in os.walk(root, topdown=True, onerror=ignore_walk_error, followlinks=False):
        directory_path = Path(directory)
        names[:] = [
            name for name in names
            if name not in SKIP_DIRS
            and not is_excluded((directory_path / name).relative_to(root), excludes)
        ]
        base = Path(directory)
        for filename in files:
            path = base / filename
            relative = path.relative_to(root)
            if is_excluded(relative, excludes):
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                if path.is_file() and path.stat().st_size <= 2_000_000:
                    yield path
            except OSError:
                continue


def collect(root: Path, max_matches: int, excludes: tuple[str, ...] = ()) -> dict:
    compiled = {name: [re.compile(p, re.IGNORECASE) for p in patterns] for name, patterns in CATEGORIES.items()}
    result = {name: [] for name in CATEGORIES}
    scanned = 0
    for path in iter_files(root, excludes):
        scanned += 1
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(lines, start=1):
            snippet = line.strip()
            if not snippet:
                continue
            for category, patterns in compiled.items():
                if len(result[category]) >= max_matches:
                    continue
                if any(pattern.search(snippet) for pattern in patterns):
                    result[category].append({
                        "path": relative,
                        "kind": classify_path(Path(relative)),
                        "line": number,
                        "text": snippet[:240],
                    })
    return {
        "root": str(root.resolve()),
        "files_scanned": scanned,
        "warning": "Matches are evidence candidates only. Inspect implementation and tests before assigning completion status.",
        "categories": result,
    }


def to_markdown(data: dict) -> str:
    rows = ["# Architecture evidence candidates", "", data["warning"], ""]
    rows.append(f"Files scanned: {data['files_scanned']}")
    for category, matches in data["categories"].items():
        rows.extend(["", f"## {category}", ""])
        if not matches:
            rows.append("No candidate found.")
            continue
        for match in matches:
            rows.append(f"1. `{match['path']}:{match['line']}` [{match['kind']}] {match['text']}")
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="Optional output path; stdout when omitted")
    parser.add_argument("--max-matches", type=int, default=30, help="Maximum matches per category")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help="Exclude a repository-relative file or directory; repeat as needed",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"root is not a directory: {root}")
    if args.max_matches < 1:
        parser.error("--max-matches must be positive")

    excludes = tuple(Path(item).as_posix().strip("/") for item in args.exclude if item.strip("/"))
    data = collect(root, args.max_matches, excludes)
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(data)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(errors="replace")
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
