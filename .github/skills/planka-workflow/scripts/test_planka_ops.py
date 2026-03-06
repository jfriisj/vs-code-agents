import unittest
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

if __name__ == "__main__":
    unittest.main()
