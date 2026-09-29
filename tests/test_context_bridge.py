import unittest

from src.context_bridge import build_context


class ContextBridgeTest(unittest.TestCase):
    def snapshot(self):
        return {
            "repository": {
                "full_name": "example/repo",
                "private": True,
                "default_branch": "main",
            },
            "files": ["README.md", "src/example.py"],
            "issues": [],
            "pull_requests": [],
            "commits": [{"sha": "abc", "message": "test"}],
            "workflow_runs": {"total_count": 1, "workflow_runs": []},
            "evidence_sources": ["example"],
            "protocol": "github-japanese-context-bridge-v0.1",
        }

    def test_read_only_human_gate(self):
        context = build_context(self.snapshot())
        self.assertEqual(context["mode"], "read_only")
        self.assertEqual(context["runtime_boundary"]["profile"], "lightweight_core")
        self.assertEqual(context["runtime_boundary"]["handoff"], "semantic_handoff")
        self.assertEqual(context["runtime_boundary"]["authority"], "HUMAN")
        self.assertFalse(context["runtime_boundary"]["repository_mutation"])
        self.assertFalse(context["action_boundary"]["repository_mutation"])
        self.assertTrue(context["action_boundary"]["human_gate_required"])

    def test_stable_evidence_and_semantic_handoff(self):
        context = build_context(self.snapshot())
        ids = [item["evidence_id"] for item in context["evidence"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(context["semantic_handoff"]["evidence_ids"], ids)
        self.assertEqual(context["semantic_handoff"]["authority"]["decision"], "HUMAN")
        self.assertFalse(context["semantic_handoff"]["authority"]["repository_mutation"])

    def test_public_perspective_boundary(self):
        context = build_context(self.snapshot())
        perspectives = context["perspectives"]
        self.assertEqual(perspectives["order"], ["ThreadRPG"])
        self.assertFalse(perspectives["authority"]["repository_mutation"])

    def test_unknown_workflow_stays_unknown(self):
        snapshot = self.snapshot()
        snapshot["workflow_runs"] = None
        context = build_context(snapshot)
        ci = next(item for item in context["evidence"] if item["role"] == "自動テスト担当")
        self.assertEqual(ci["type"], "UNKNOWN")

    def test_language_changes_presentation_only(self):
        snapshot = self.snapshot()
        ja = build_context(snapshot, explanation_level=3, language="ja")
        en = build_context(snapshot, explanation_level=3, language="en")
        self.assertNotEqual(ja["human_explanation"], en["human_explanation"])
        self.assertEqual(ja["evidence"], en["evidence"])
        self.assertEqual(ja["perspectives"], en["perspectives"])
        self.assertEqual(en["language"], "en")


if __name__ == "__main__":
    unittest.main()
