"""Case discovery contracts, using only temporary public-style targets."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from saygo.qa import cases


class CaseDiscoveryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.tests = self.root / "tests"
        self.target = self.tests / "example"
        self.case_dir = self.target / "cases"
        self.case_dir.mkdir(parents=True)
        patcher = patch.object(cases, "TESTS_DIR", self.tests)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write_case(self, name, text):
        path = self.case_dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_absolute_markdown_target_scans_feature_tree_once(self):
        self.write_case("second.md", "### TC-002\nSecond")
        self.write_case("first.md", "### TC-001\nFirst")
        with patch.object(cases, "_collect_feature_cases", wraps=cases._collect_feature_cases) as collect:
            discovered, target = cases._resolve_test_target(str(self.target))
        self.assertEqual(discovered, ["### TC-001\nFirst", "### TC-002\nSecond"])
        self.assertEqual(target, self.target)
        collect.assert_called_once_with(self.target)

    def test_feature_precedence_and_nested_target_ownership(self):
        (self.target / "README.md").write_text("Example target", encoding="utf-8")
        (self.case_dir / "README.md").write_text("Nested target", encoding="utf-8")
        feature = self.write_case("first.feature", "Feature: Example\n  Scenario: Open page\n    Given a page\n")
        markdown = self.write_case("legacy.md", "### TC-001\nLegacy")
        feature_cases, target = cases._resolve_test_target("example")
        self.assertEqual(len(feature_cases), 1)
        self.assertIn("Open page", feature_cases[0])
        self.assertNotIn("Legacy", feature_cases[0])
        self.assertEqual(target, self.target)
        self.assertEqual(cases._resolve_test_target("example/cases/first.feature"),
                         (feature_cases, self.case_dir))
        self.assertEqual(cases._resolve_test_target(str(feature)), (feature_cases, self.case_dir))
        self.assertEqual(cases._resolve_test_target(str(markdown)), (["### TC-001\nLegacy"], self.target))

    def test_context_uses_top_level_target_and_rejects_outside_paths(self):
        account = {"email": "${EMAIL}"}
        (self.target / "_accounts.json").write_text(json.dumps([account]), encoding="utf-8")
        (self.target / "_preconditions.md").write_text("Recover the welcome screen.\n", encoding="utf-8")
        self.assertEqual(cases._load_accounts(self.case_dir), [account])
        self.assertEqual(cases._load_preconditions(self.case_dir), "Recover the welcome screen.")
        for path in (None, self.tests, self.root):
            with self.subTest(path=path):
                self.assertEqual(cases._load_accounts(path), [])
                self.assertIsNone(cases._load_preconditions(path))

    def test_legacy_subtarget_external_file_and_missing_paths(self):
        self.write_case("legacy.md", "### TC-001\nLegacy")
        self.assertEqual(cases._resolve_test_target("example/legacy"), (["### TC-001\nLegacy"], self.target))
        self.assertEqual(cases._resolve_test_target("example/cases/legacy.md"),
                         (["### TC-001\nLegacy"], self.target))
        external = self.root / "external.txt"
        external.write_text("Ad hoc case", encoding="utf-8")
        self.assertEqual(cases._resolve_test_target(str(external)), (["Ad hoc case"], None))
        for suffix in ("feature", "md", "txt"):
            with self.subTest(suffix=suffix), self.assertRaisesRegex(SystemExit, "test file not found"):
                cases._resolve_test_target(str(self.root / f"missing.{suffix}"))
        self.assertEqual(cases._resolve_test_target("Check the welcome screen"),
                         (["Check the welcome screen"], None))
