import unittest

from src.perspectives import build_perspectives, thread_rpg


class PerspectivesTests(unittest.TestCase):
    def evidence(self):
        return [
            {
                "evidence_id": "ev-a",
                "role": "問題・要望担当",
                "source": "GitHub Issues",
                "type": "FACT",
                "observation": {"title": "A"},
            },
            {
                "evidence_id": "ev-b",
                "role": "自動テスト担当",
                "source": "GitHub Actions",
                "type": "UNKNOWN",
                "observation": {"note": "not observed"},
            },
            {
                "evidence_id": "ev-c",
                "role": "問題・要望担当",
                "source": "GitHub Issues",
                "type": "FACT",
                "observation": {"title": "B"},
            },
        ]

    def test_thread_rpg_preserves_evidence(self):
        result = thread_rpg(self.evidence())
        self.assertEqual([x["evidence_id"] for x in result["threads"]], ["ev-a", "ev-b", "ev-c"])
        self.assertEqual(result["authority"]["decision"], "HUMAN")

    def test_complete_stack_has_public_boundary(self):(self):
        result = build_perspectives(self.evidence())
        self.assertEqual(result["order"][2:], ["ThreadRPG"])
        self.assertEqual(result["authority"]["decision"], "HUMAN")
        self.assertFalse(result["authority"]["repository_mutation"])


if __name__ == "__main__":
    unittest.main()
