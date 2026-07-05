#!/usr/bin/env python3
"""Regression tests for the ArchProof evidence candidate scanner."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("collect_architecture_evidence.py")
SPEC = importlib.util.spec_from_file_location("archproof_scanner", MODULE_PATH)
assert SPEC and SPEC.loader
SCANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCANNER)


class EvidenceScannerTest(unittest.TestCase):
    def test_classifies_implementation_test_and_deployment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "tests").mkdir()
            (root / "deploy").mkdir()
            (root / "src" / "consumer.py").write_text("# idempotent outbox consumer\n", encoding="utf-8")
            (root / "tests" / "test_consumer.py").write_text("def test_redelivery(): assert True\n", encoding="utf-8")
            (root / "deploy" / "app.yaml").write_text("kind: Deployment\n", encoding="utf-8")

            data = SCANNER.collect(root, 20)

            messaging_kinds = {item["kind"] for item in data["categories"]["messaging-reliability"]}
            deployment_kinds = {item["kind"] for item in data["categories"]["deployment"]}
            self.assertIn("implementation", messaging_kinds)
            self.assertIn("test", messaging_kinds)
            self.assertIn("deployment", deployment_kinds)

    def test_excludes_relative_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "generated").mkdir()
            (root / "generated" / "noise.md").write_text("RabbitTemplate outbox\n", encoding="utf-8")

            data = SCANNER.collect(root, 20, ("generated",))

            self.assertEqual(0, data["files_scanned"])
            self.assertFalse(data["categories"]["messaging-reliability"])


if __name__ == "__main__":
    unittest.main()
