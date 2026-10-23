
import unittest
from dce_optimizer import eliminate_dead_code


class TestDeadCodeElimination(unittest.TestCase):

    def test_unused_assignment_is_removed(self):
        code = """
x = 10
y = 20
print(x)
"""
        result = eliminate_dead_code(code)

        self.assertIn("x = 10", result["optimized_code"])
        self.assertNotIn("y = 20", result["optimized_code"])
        self.assertEqual(result["removed_count"], 1)

    def test_used_assignments_are_preserved(self):
        code = """
a = 10
b = a + 5
print(b)
"""
        result = eliminate_dead_code(code)

        self.assertEqual(
            result["optimized_code"],
            ["a = 10", "b = a + 5", "print(b)"]
        )
        self.assertEqual(result["removed_count"], 0)

    def test_overwritten_assignment_is_removed(self):
        code = """
x = 10
x = 20
print(x)
"""
        result = eliminate_dead_code(code)

        self.assertNotIn("x = 10", result["optimized_code"])
        self.assertIn("x = 20", result["optimized_code"])

    def test_print_statement_is_preserved(self):
        code = """
x = 10
print("Hello")
"""
        result = eliminate_dead_code(code)

        self.assertIn('print("Hello")', result["optimized_code"])

    def test_side_effecting_call_is_preserved(self):
        code = """
x = readInput()
print("Finished")
"""
        result = eliminate_dead_code(code)

        self.assertIn("x = readInput()", result["optimized_code"])

    def test_instruction_counts(self):
        code = """
a = 1
b = 2
print(a)
"""
        result = eliminate_dead_code(code)

        self.assertEqual(result["original_count"], 3)
        self.assertEqual(result["optimized_count"], 2)
        self.assertEqual(result["removed_count"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
