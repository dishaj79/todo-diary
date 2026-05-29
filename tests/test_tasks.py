# ============================================================
#  tests/test_tasks.py  —  Unit Tests
# ============================================================
#
#  CONCEPT: Unit Testing
#  A unit test checks that a small piece of code (a "unit")
#  works correctly. You write tests so that:
#    1. You know your code works RIGHT NOW
#    2. If you change something later, tests catch breakage
#
#  Python's built-in 'unittest' module provides:
#    - TestCase class to group related tests
#    - assert methods to check expected vs actual values
#
#  Run all tests with:  python -m pytest tests/   (or python -m unittest discover)
# ============================================================

import sys
import os
import unittest

# Add parent directory to path so we can import task.py and diary.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task import Task
from diary import Diary


# ── Testing the Task class ─────────────────────────────────

class TestTask(unittest.TestCase):
    """Tests for the Task class."""

    def setUp(self):
        """
        CONCEPT: setUp runs BEFORE every test method.
        It's like setting up your desk before starting work.
        We create a fresh task so each test starts clean.
        """
        self.task = Task("Buy groceries", "Milk and eggs", "high", "personal")

    def test_task_creation(self):
        """A newly created task should have correct default values."""
        self.assertEqual(self.task.title, "Buy groceries")
        self.assertEqual(self.task.description, "Milk and eggs")
        self.assertEqual(self.task.priority, "high")
        self.assertEqual(self.task.category, "personal")
        self.assertFalse(self.task.done)           # Should start as NOT done
        self.assertIsNone(self.task.completed_at)  # No completion time yet

    def test_mark_done(self):
        """Marking a task done should set done=True and record completion time."""
        self.task.mark_done()
        self.assertTrue(self.task.done)
        self.assertIsNotNone(self.task.completed_at)  # Should now have a timestamp

    def test_mark_pending(self):
        """Undoing a completed task should reset done=False."""
        self.task.mark_done()    # First mark it done
        self.task.mark_pending() # Then undo it
        self.assertFalse(self.task.done)
        self.assertIsNone(self.task.completed_at)

    def test_to_dict(self):
        """to_dict() should return a dictionary with all task fields."""
        d = self.task.to_dict()
        self.assertIsInstance(d, dict)           # Should be a dict
        self.assertIn("title", d)                # Should have a 'title' key
        self.assertEqual(d["title"], "Buy groceries")

    def test_from_dict(self):
        """from_dict() should recreate a Task from a dictionary."""
        d = self.task.to_dict()
        restored = Task.from_dict(d)
        self.assertEqual(restored.title, self.task.title)
        self.assertEqual(restored.priority, self.task.priority)

    def test_default_values(self):
        """Task created with only a title should have sensible defaults."""
        t = Task("Quick task")
        self.assertEqual(t.description, "")
        self.assertEqual(t.priority, "medium")
        self.assertEqual(t.category, "general")


# ── Testing the Diary class ────────────────────────────────

class TestDiary(unittest.TestCase):
    """Tests for the Diary class."""

    def setUp(self):
        """Use a temp file so tests don't touch real data."""
        self.test_file = "data/test_tasks_temp.json"
        self.diary = Diary(filepath=self.test_file)
        self.diary.tasks = []  # Always start with empty tasks

    def tearDown(self):
        """
        CONCEPT: tearDown runs AFTER every test — cleanup time!
        We delete the temp file so tests don't leave junk behind.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        """Adding a task should increase the task count by 1."""
        self.diary.add_task("Test task")
        self.assertEqual(len(self.diary.tasks), 1)
        self.assertEqual(self.diary.tasks[0].title, "Test task")

    def test_add_multiple_tasks(self):
        """Should be able to add many tasks."""
        self.diary.add_task("Task 1")
        self.diary.add_task("Task 2")
        self.diary.add_task("Task 3")
        self.assertEqual(len(self.diary.tasks), 3)

    def test_complete_task(self):
        """Completing task #1 should mark it done."""
        self.diary.add_task("My task")
        self.diary.complete_task(1)
        self.assertTrue(self.diary.tasks[0].done)

    def test_delete_task(self):
        """Deleting a task should remove it from the list."""
        self.diary.add_task("Task to delete")
        self.diary.delete_task(1)
        self.assertEqual(len(self.diary.tasks), 0)

    def test_search_finds_match(self):
        """Search should find tasks containing the keyword."""
        self.diary.add_task("Buy apples")
        self.diary.add_task("Read a book")
        # We check that search runs without error (output goes to terminal)
        # A more thorough test would capture output — that's an advanced topic!
        self.diary.search("apple")

    def test_invalid_priority_defaults_to_medium(self):
        """An invalid priority should silently default to 'medium'."""
        self.diary.add_task("Task", priority="INVALID")
        self.assertEqual(self.diary.tasks[0].priority, "medium")

    def test_clear_done(self):
        """clear_done should remove only completed tasks."""
        self.diary.add_task("Task A")
        self.diary.add_task("Task B")
        self.diary.complete_task(1)   # Mark Task A as done
        self.diary.clear_done()
        self.assertEqual(len(self.diary.tasks), 1)
        self.assertEqual(self.diary.tasks[0].title, "Task B")

    def test_persistence(self):
        """Tasks saved to file should survive a reload."""
        self.diary.add_task("Persistent task", priority="high")
        # Create a NEW diary pointing at the same file
        reloaded = Diary(filepath=self.test_file)
        self.assertEqual(len(reloaded.tasks), 1)
        self.assertEqual(reloaded.tasks[0].title, "Persistent task")


# ── Run tests ──────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)