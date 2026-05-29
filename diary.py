# ============================================================
#  diary.py  —  The Diary (manages all tasks)
# ============================================================
#
#  CONCEPTS covered here:
#  - Lists  (storing multiple tasks)
#  - Loops  (for ... in ...)
#  - File I/O  (reading & writing files)
#  - JSON  (a format for saving structured data)
#  - List comprehensions  (powerful one-line filters)
#  - try / except  (handling errors gracefully)
#  - os module  (checking if a file exists)
# ============================================================

import json   # Built-in module to read/write JSON files
import os     # Built-in module for file system operations
 
from task import Task


class Diary:
    """
    Manages a collection of Task objects.
    Handles adding, deleting, listing, searching, and saving.
    """
    def __init__(self, filepath="data/tasks.json"):
        self.filepath = filepath   # Where we save/load tasks
        self.tasks    = []         # Empty list to start
        self._load()               # Load any previously saved tasks
    
    
    # ── ADD ────────────────────────────────────────────────────
 
    def add_task(self, title, description="", priority="medium", category="general"):
        """Create a new Task and add it to our list."""
 
        # CONCEPT: Validation with 'in' operator
        # 'in' checks if a value exists inside a list/string
        valid_priorities = ["low", "medium", "high"]
        if priority not in valid_priorities:
            print(f"⚠️  Invalid priority '{priority}'. Using 'medium'.")
            priority = "medium"

        # CONCEPT: Creating an object from a class
        new_task = Task(title, description, priority, category)

        # .append() adds an item to the END of a list
        self.tasks.append(new_task)
        self._save()
 
        print(f"🆕 Task added: '{title}'")
        return new_task
    

     # ── VIEW ───────────────────────────────────────────────────
 
    def list_tasks(self, show="all", category=None, priority=None):
        """
        Print tasks to the screen.
        show = "all" | "done" | "pending"
        """
 
        # CONCEPT: List comprehension — a compact way to filter a list
        # Long version:
        #   filtered = []
        #   for t in self.tasks:
        #       if condition:
        #           filtered.append(t)
        #
        # Short version (list comprehension):
        #   filtered = [t for t in self.tasks if condition]
 
        filtered = self.tasks  # Start with all tasks
 
        if show == "done":
            filtered = [t for t in filtered if t.done]
        elif show == "pending":
            filtered = [t for t in filtered if not t.done]
 
        if category:
            # .lower() makes comparison case-insensitive
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
 
        if priority:
            filtered = [t for t in filtered if t.priority.lower() == priority.lower()]
 
        # CONCEPT: Early return
        # If nothing to show, exit the function early
        if not filtered:
            print("📭 No tasks found.")
            return
 
        print(f"\n{'='*50}")
        print(f"  📔 YOUR TASKS  ({len(filtered)} found)")
        print(f"{'='*50}")
 
        # CONCEPT: enumerate() gives you index + value together
        # Without enumerate: for task in filtered
        # With enumerate:    for i, task in enumerate(filtered, start=1)
        for i, task in enumerate(filtered, start=1):
            print(f"\n  [{i}] {task}")
 
        print(f"\n{'='*50}\n")


     # ── COMPLETE / UNDO ────────────────────────────────────────
 
    def complete_task(self, index):
        """Mark a task as done by its display number (1-based)."""
        task = self._get_task(index)
        if task:
            task.mark_done()
            self._save()
 
    def undo_task(self, index):
        """Mark a task as pending again."""
        task = self._get_task(index)
        if task:
            task.mark_pending()
            self._save()

    
    # ── DELETE ─────────────────────────────────────────────────
 
    def delete_task(self, index):
        """Remove a task permanently."""
        task = self._get_task(index)
        if task:
            # .remove() deletes the first matching item from a list
            self.tasks.remove(task)
            self._save()
            print(f"🗑️  Deleted: '{task.title}'")
 
    def clear_done(self):
        """Remove all completed tasks at once."""
 
        # CONCEPT: List comprehension used for FILTERING (keeping only pending)
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        removed = before - len(self.tasks)
        self._save()
        print(f"🧹 Cleared {removed} completed task(s).")


    # ── SEARCH ─────────────────────────────────────────────────
 
    def search(self, keyword):
        """Find tasks whose title or description contains the keyword."""
 
        # CONCEPT: 'in' operator on strings checks for substrings
        # "hello" in "say hello world"  →  True
        # .lower() makes it case-insensitive
 
        keyword = keyword.lower()
        results = [
            t for t in self.tasks
            if keyword in t.title.lower() or keyword in t.description.lower()
        ]
 
        if not results:
            print(f"🔍 No tasks found matching '{keyword}'.")
            return
 
        print(f"\n🔍 Search results for '{keyword}':")
        for i, task in enumerate(results, start=1):
            print(f"\n  [{i}] {task}")
        print()


    # ── STATS ──────────────────────────────────────────────────
 
    def show_stats(self):
        """Display a summary of your tasks."""
        total   = len(self.tasks)
        done    = sum(1 for t in self.tasks if t.done)      # sum() with a generator
        pending = total - done
 
        # CONCEPT: Conditional expression (ternary)
        # value = X if condition else Y
        pct = f"{(done/total*100):.0f}%" if total > 0 else "N/A"
 
        print(f"""
╔══════════════════════════════╗
║       📊 DIARY STATS         ║
╠══════════════════════════════╣
║  Total tasks   : {total:<12}║
║  ✅ Done       : {done:<12}║
║  ⏳ Pending    : {pending:<12}║
║  Completion    : {pct:<12}║
╚══════════════════════════════╝
        """)


    # ── PRIVATE HELPERS (convention: _ prefix) ─────────────────
    #
    # CONCEPT: Private methods
    # Methods starting with _ are "private by convention" — they're
    # internal helpers, not meant to be called from outside the class.
 
    def _get_task(self, index):
        """Get a task by its 1-based display index. Returns None if invalid."""
 
        # CONCEPT: try/except — handling errors without crashing
        # If the user types "abc" instead of a number, we catch the error.
        try:
            i = int(index) - 1           # Convert to 0-based index
            if 0 <= i < len(self.tasks): # Check it's within range
                return self.tasks[i]
            else:
                print(f"⚠️  No task at position {index}. You have {len(self.tasks)} task(s).")
                return None
        except ValueError:
            print("⚠️  Please enter a valid number.")
            return None
        

    def _save(self):
        """Save all tasks to a JSON file."""
 
        # CONCEPT: os.makedirs — create the folder if it doesn't exist
        # exist_ok=True means "don't error if folder already exists"
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
 
        # CONCEPT: File I/O
        # open(path, "w") opens a file for Writing (creates it if missing)
        # 'with' ensures the file is properly closed even if an error occurs
        with open(self.filepath, "w") as f:
            # json.dump() converts Python objects → JSON text and writes to file
            # indent=2 makes it human-readable (pretty-printed)
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)


    def _load(self):
        """Load tasks from the JSON file (if it exists)."""
 
        # CONCEPT: os.path.exists — check if a file/folder exists
        if not os.path.exists(self.filepath):
            return   # No file yet — start fresh, that's fine
 
        try:
            # open(path, "r") opens a file for Reading
            with open(self.filepath, "r") as f:
                data = json.load(f)   # JSON text → Python list of dicts
 
            # Recreate Task objects from the saved dictionaries
            self.tasks = [Task.from_dict(d) for d in data]
            print(f"📂 Loaded {len(self.tasks)} task(s) from diary.")
 
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Could not load tasks: {e}. Starting fresh.")
            self.tasks = []
    

    