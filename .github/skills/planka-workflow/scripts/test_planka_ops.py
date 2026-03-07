import unittest
from planka_ops import _build_phase_comment
from planka_ops import _find_task
from planka_ops import _parse_task_ids
from planka_ops import _phase_comment_key
from planka_ops import parse_value


class TestPlankaOps(unittest.TestCase):
    def test_id_remains_string(self):
        # Even if numeric, fields ending in 'Id' should remain strings
        self.assertEqual(parse_value("12345", "cardId"), "12345")
        self.assertIsInstance(parse_value("12345", "cardId"), str)
        self.assertEqual(parse_value("001", "projectId"), "001")

    def test_position_becomes_int(self):
        # Fields in the TYPE_MAP should be cast to their mapped type
        self.assertEqual(parse_value("10", "position"), 10)
        self.assertIsInstance(parse_value("10", "position"), int)

    def test_bool_becomes_bool(self):
        # Booleans should be correctly cast
        self.assertTrue(parse_value("true", "isCompleted"))
        self.assertIsInstance(parse_value("true", "isCompleted"), bool)
        self.assertFalse(parse_value("false", "enabled"))

    def test_unknown_field_becomes_int(self):
        # Fields that are not IDs or Booleans, but look like digits, become int
        self.assertEqual(parse_value("999", "unknownField"), 999)
        self.assertIsInstance(parse_value("999", "unknownField"), int)

    def test_phase_comment_key_default(self):
        key = _phase_comment_key(
            {
                "agent": "qa",
                "phase": "QA",
                "artifact": "agent-output/qa/001-core-handoff-lifecycle-qa.md",
            }
        )
        self.assertEqual(key, "qa|QA|agent-output/qa/001-core-handoff-lifecycle-qa.md")

    def test_build_phase_comment_schema(self):
        text = _build_phase_comment(
            {
                "agent": "devops",
                "phase": "Release",
                "artifact": "agent-output/deployment/v0.1.0.md",
                "status": "COMPLETE",
                "verdict": "RELEASE_READY",
                "next": "retrospective",
            }
        )
        self.assertIn("[PHASE_CLOSE]", text)
        self.assertIn("Agent: devops", text)
        self.assertIn("Phase: Release", text)
        self.assertIn("Verdict: RELEASE_READY", text)
        self.assertIn("Artifact: agent-output/deployment/v0.1.0.md", text)
        self.assertIn("Next: retrospective", text)

    def test_parse_task_ids_variants(self):
        self.assertEqual(_parse_task_ids(["1", "2"]), ["1", "2"])
        self.assertEqual(_parse_task_ids("1,2, 3"), ["1", "2", "3"])
        self.assertEqual(_parse_task_ids("1724974073588483623"), ["1724974073588483623"])
        self.assertEqual(_parse_task_ids(None), [])

    def test_find_task_matches_top_level_tasks(self):
        card = {
            "tasks": [
                {"id": "t1", "taskListId": "list-1", "name": "Verify log redaction"},
                {"id": "t2", "taskListId": "list-2", "name": "Other task"},
            ]
        }
        task = _find_task(card, "list-1", "verify   log   redaction")
        self.assertIsNotNone(task)
        self.assertEqual(task.get("id"), "t1")


if __name__ == "__main__":
    unittest.main()
