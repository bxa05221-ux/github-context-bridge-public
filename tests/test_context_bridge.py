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

    def test_maintenance_conference_preserves_human_gate(self):
        context = build_context(self.snapshot())

        self.assertEqual(context["mode"], "read_only")
        self.assertEqual(context["runtime_boundary"]["profile"], "lightweight_core")
        self.assertTrue(context["runtime_boundary"]["heavy_use_boundary"])
        self.assertEqual(context["runtime_boundary"]["handoff"], "semantic_handoff")
        self.assertEqual(context["runtime_boundary"]["authority"], "HUMAN")
        self.assertFalse(context["runtime_boundary"]["repository_mutation"])
        self.assertFalse(context["action_boundary"]["repository_mutation"])
        self.assertTrue(context["action_boundary"]["human_gate_required"])
        self.assertIn(
            "pull_request_inspection",
            context["action_boundary"]["observed_capabilities"],
        )
        self.assertEqual(context["保守安価"]["name"], "保守安価")
        self.assertEqual(context["保守安価"]["decision_authority"], "HUMAN")
        self.assertTrue(context["human_gate"]["required"])

        roles = {item["role"] for item in context["roles"]}
        self.assertIn("事実確認担当", roles)
        self.assertIn("ルール担当", roles)

    def test_context_exposes_stable_evidence_and_semantic_handoff(self):
        context = build_context(self.snapshot())

        self.assertTrue(context["evidence"])
        ids = [item["evidence_id"] for item in context["evidence"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(context["semantic_handoff"]["evidence_ids"], ids)
        self.assertEqual(
            context["semantic_handoff"]["authority"]["decision"], "HUMAN"
        )
        self.assertFalse(
            context["semantic_handoff"]["authority"]["repository_mutation"]
        )

    def test_perspectives_preserve_evidence_ids_and_boundary(self):
        context = build_context(self.snapshot())
        ids = [item["evidence_id"] for item in context["evidence"]]
        perspectives = context["perspectives"]

        self.assertEqual(
            perspectives["perspective_stack"]["thread_rpg"]["threads"][0]["evidence_id"],
            ids[0],
        )
        self.assertEqual(perspectives["order"], ["ThreadRPG"])
        self.assertEqual(
            perspectives["perspective_stack"]["phase_rotation_eisenhower"]["status"],
            "boundary_only",
        )
        self.assertEqual(
            perspectives["perspective_stack"]["distorted_sphere"]["status"],
            "boundary_only",
        )
        self.assertIsNone(
            perspectives["perspective_stack"]["distorted_sphere"]["geometry"]
        )
        self.assertFalse(perspectives["authority"]["repository_mutation"])

    def test_perspectives_never_promote_unknown_to_fact(self):
        snapshot = self.snapshot()
        snapshot["workflow_runs"] = None

        context = build_context(snapshot)
        ci_evidence = next(
            item
            for item in context["evidence"]
            if item["role"] == "自動テスト担当"
        )

        self.assertEqual(ci_evidence["type"], "UNKNOWN")
        thread = context["perspectives"]["perspective_stack"]["thread_rpg"]
        ci_thread = next(
            item for item in thread["threads"]
            if item["role"] == "自動テスト担当"
        )
        self.assertEqual(ci_thread["type"], "UNKNOWN")


    def test_missing_workflow_evidence_remains_unknown(self):
        snapshot = {
            "files": [],
            "issues": [],
            "pull_requests": [],
            "commits": [],
            "workflow_runs": None,
        }

        context = build_context(snapshot)
        ci = next(
            item for item in context["roles"]
            if item["role"] == "自動テスト担当"
        )

        self.assertEqual(ci["type"], "UNKNOWN")
        self.assertIn("まだ確認できていません", context["human_explanation"])

    def test_explanation_level_changes_presentation_only(self):
        context_plain = build_context(self.snapshot(), explanation_level=1)
        context_deep = build_context(self.snapshot(), explanation_level=5)

        self.assertNotEqual(
            context_plain["human_explanation"],
            context_deep["human_explanation"],
        )
        self.assertEqual(context_plain["roles"], context_deep["roles"])
        self.assertEqual(context_plain["保守安価"], context_deep["保守安価"])
        self.assertEqual(context_plain["human_gate"], context_deep["human_gate"])
        self.assertEqual(context_plain["evidence"], context_deep["evidence"])
        self.assertEqual(context_plain["perspectives"], context_deep["perspectives"])

        self.assertNotIn("保守安価", context_plain["human_explanation"])
        self.assertIn("保守安価", context_deep["human_explanation"])
        self.assertIn("Human Gate", context_deep["human_explanation"])

    def test_explanation_level_is_bounded(self):
        low = build_context(self.snapshot(), explanation_level=0)
        high = build_context(self.snapshot(), explanation_level=99)

        self.assertEqual(low["explanation_profile"]["level"], 1)
        self.assertEqual(high["explanation_profile"]["level"], 5)
        self.assertTrue(low["explanation_profile"]["evidence_invariant"])
        self.assertTrue(high["explanation_profile"]["user_controlled"])

    def test_causal_chain_is_preserved_across_explanation_levels(self):
        snapshot = self.snapshot()
        snapshot["causal_chain"] = {
            "issue_to_pr": "CONFIRMED",
            "pr_to_commit": "CONFIRMED",
            "commit_to_workflow": "UNKNOWN",
            "pr_to_merge": "UNKNOWN",
            "workflow_to_merge": "UNKNOWN",
        }
        plain = build_context(snapshot, explanation_level=1)
        technical = build_context(snapshot, explanation_level=3)

        self.assertEqual(plain["causal_chain"], technical["causal_chain"])
        self.assertIn("Issue→PR=CONFIRMED", technical["human_explanation"])
        self.assertIn("Commit→Workflow=UNKNOWN", technical["human_explanation"])

    def test_change_lineage_is_exposed_without_changing_human_gate(self):
        snapshot = self.snapshot()
        snapshot["pull_requests"] = [{
            "number": 3,
            "title": "example change",
            "state": "closed",
            "merged": True,
            "head_sha": "abc",
            "merge_commit_sha": "def",
            "changed_files": [
                {"filename": "src/example.py", "status": "modified"}
            ],
            "reviews": [{"state": "APPROVED"}],
        }]
        snapshot["causal_chain"] = {
            "issue_to_pr": "UNKNOWN",
            "pr_to_commit": "CONFIRMED",
            "commit_to_workflow": "UNKNOWN",
            "pr_to_merge": "CONFIRMED",
            "workflow_to_merge": "UNKNOWN",
        }
        context = build_context(snapshot, explanation_level=5)

        self.assertEqual(
            context["change_lineage"]["pull_requests"][0]["number"], 3
        )
        self.assertEqual(
            context["change_lineage"]["causal_chain"]["pr_to_merge"], "CONFIRMED"
        )
        self.assertEqual(
            context["change_lineage"]["causal_chain"]["workflow_to_merge"], "UNKNOWN"
        )
        self.assertTrue(context["human_gate"]["required"])
        self.assertEqual(context["human_gate"]["authority"], "HUMAN")

    def test_language_changes_presentation_only(self):
        snapshot = self.snapshot()
        ja = build_context(snapshot, explanation_level=3, language="ja")
        en = build_context(snapshot, explanation_level=3, language="en")

        self.assertNotEqual(ja["human_explanation"], en["human_explanation"])
        self.assertEqual(ja["causal_chain"], en["causal_chain"])
        self.assertEqual(ja["roles"], en["roles"])
        self.assertEqual(ja["human_gate"], en["human_gate"])
        self.assertEqual(ja["evidence"], en["evidence"])
        self.assertEqual(ja["perspectives"], en["perspectives"])
        self.assertEqual(en["language"], "en")

    def test_user_profile_is_presentation_only(self):
        snapshot = self.snapshot()
        context = build_context(snapshot, explanation_level=2, language="en")
        profile = context["explanation_profile"]

        self.assertEqual(profile["language"], "en")
        self.assertEqual(profile["explanation_level"], 2)
        self.assertTrue(profile["user_controlled"])
        self.assertTrue(profile["evidence_invariant"])
        self.assertTrue(profile["authority_invariant"])
        self.assertTrue(context["human_gate"]["required"])


if __name__ == "__main__":
    unittest.main()
