import unittest

from src.evidence import build_evidence_record, evidence_id, semantic_handoff


class EvidenceTest(unittest.TestCase):
    def test_evidence_id_is_stable(self):
        observation = {"state": "open", "number": 29}
        first = evidence_id("変更担当", "GitHub Pull Requests", "FACT", observation)
        second = evidence_id("変更担当", "GitHub Pull Requests", "FACT", observation)
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("ev-"))

    def test_different_evidence_has_different_id(self):
        first = evidence_id("変更担当", "GitHub Pull Requests", "FACT", {"state": "open"})
        second = evidence_id("変更担当", "GitHub Pull Requests", "FACT", {"state": "closed"})
        self.assertNotEqual(first, second)

    def test_handoff_keeps_human_authority(self):
        record = build_evidence_record(
            "事実確認担当",
            "cross-source verification",
            "FACT",
            {"repository": "example/repo"},
        )
        handoff = semantic_handoff({"evidence": [record], "mode": "read_only"})
        self.assertEqual(handoff["evidence_ids"], [record["evidence_id"]])
        self.assertEqual(handoff["authority"]["decision"], "HUMAN")
        self.assertFalse(handoff["authority"]["repository_mutation"])


if __name__ == "__main__":
    unittest.main()
