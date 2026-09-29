"""Real-world validation fixture for the public GitHub Context Bridge."""

import unittest

from src.context_bridge import build_context


class RealWorldValidationTests(unittest.TestCase):
    def test_github_shaped_observations_complete_read_only_handoff(self):
        snapshot = {
            "repository": {
                "full_name": "example/project",
                "default_branch": "main",
            },
            "issues": [{"number": 12, "title": "Document the explanation flow", "state": "open"}],
            "pull_requests": [{"number": 7, "title": "docs: explain the bridge", "state": "open", "merged": False}],
            "commits": [{"sha": "abc123", "message": "docs: explain the bridge"}],
            "workflow_runs": [],
            "evidence_sources": ["GitHub"],
            "protocol": "github-japanese-context-bridge-v0.1",
        }
        context = build_context(snapshot)
        self.assertEqual(context["mode"], "read_only")
        self.assertTrue(context["evidence"])
        self.assertTrue(context["semantic_handoff"]["evidence_ids"])
        self.assertEqual(context["semantic_handoff"]["authority"]["decision"], "HUMAN")
        self.assertFalse(context["semantic_handoff"]["authority"]["repository_mutation"])
        self.assertEqual(context["runtime_boundary"]["profile"], "public_core")
        self.assertEqual(context["perspectives"]["order"], ["ThreadRPG"])

        workflow = next(item for item in context["evidence"] if item["role"] == "自動テスト担当")
        self.assertEqual(workflow["type"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
