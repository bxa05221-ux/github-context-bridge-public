"""Real-world validation fixture for the GitHub Context Bridge.

This test deliberately uses GitHub-shaped observations rather than abstract
strings. It validates the complete read-only handoff path without granting
repository mutation authority.
"""

import unittest

from src.context_bridge import build_context


class RealWorldValidationTests(unittest.TestCase):
    def test_github_shaped_observations_complete_read_only_handoff(self):
        context = build_context(
            repository={
                "full_name": "example/project",
                "default_branch": "main",
            },
            issues=[
                {
                    "number": 12,
                    "title": "Document the Japanese explanation flow",
                    "state": "open",
                }
            ],
            pulls=[
                {
                    "number": 7,
                    "title": "docs: explain the bridge",
                    "state": "open",
                    "merged": False,
                }
            ],
            commits=[
                {
                    "sha": "abc123",
                    "message": "docs: explain the bridge",
                }
            ],
            workflow_runs=[],
        )

        self.assertEqual(context["mode"], "read_only")
        self.assertTrue(context["evidence"])
        self.assertTrue(context["semantic_handoff"]["evidence_ids"])

        self.assertEqual(
            context["semantic_handoff"]["authority"]["decision"],
            "HUMAN",
        )
        self.assertFalse(
            context["semantic_handoff"]["authority"]["repository_mutation"]
        )

        self.assertEqual(
            context["runtime_boundary"]["profile"],
            "lightweight_core",
        )
        self.assertTrue(context["runtime_boundary"]["heavy_use_boundary"])

        self.assertEqual(
            context["perspectives"]["order"][2:],
            ["ThreadRPG"],
        )

        workflow_evidence = [
            item
            for item in context["evidence"]
            if item.get("type") == "workflow"
        ]
        for item in workflow_evidence:
            self.assertEqual(item.get("observation"), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
