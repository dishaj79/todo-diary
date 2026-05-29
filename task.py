# ============================================================
#  task.py  —  The Task "blueprint"
# ============================================================
#
#  CONCEPT: Classes & OOP
#  A class is like a BLUEPRINT. Just like a house blueprint
#  lets you build many houses, a class lets you create many
#  task objects — each with its own data.
#
#  Think of it this way:
#    Class  = Blueprint of a Task
#    Object = An actual task (e.g. "Buy groceries")
# ============================================================

from datetime import datetime   # Built-in module to work with dates & times


class Task:
    """Represent a single ToDo task."""
    # ----------------------------------------------------------
    # __init__ is the CONSTRUCTOR — it runs automatically when
    # you create a new Task. Like filling out a form when you
    # register somewhere.
    #
    # 'self' always refers to the specific object being created.
    # Think of 'self' as "this particular task".
    #
    # Parameters with = have DEFAULT VALUES, so they're optional.
    # ----------------------------------------------------------

    def __init__(self, title, description="", priority="medium", category="general"):
        self.title=title               # str  — what the task is
        self.description=description   # str  — extra detail (optional)
        self.priority=priority         # str  — "low" | "medium" | "high"
        self.category=category         # str  — e.g. "work", "personal"
        self.done=False                # bool — False = pending, True = done

        # datetime.now() gives the current date and time
        # .strftime() formats it into a readable string
        self.created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        self.completed_at=None         # Will be set when task is marked done


    # ----------------------------------------------------------
    # CONCEPT: Methods
    # A method is just a function that belongs to a class.
    # It always takes 'self' as the first argument.
    # ----------------------------------------------------------

    def mark_done(self):
        """Mark this task as completed."""
        self.done=True
        self.completed_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"'{self.title}' marked as done! ")
    

    def mark_pending(self):
        """Undo — mark this task as not completed."""
        self.done=False
        self.completed_at=None
        print(f"'{self.title}' marked as pending! ")

    
    # ----------------------------------------------------------
    # CONCEPT: to_dict()
    # We convert the Task to a plain Python dictionary so we
    # can save it to a JSON file later.
    # A dict looks like: {"key": "value", "key2": "value2"}
    # ----------------------------------------------------------

    def to_dict(self):
        """Convert task to a dictionary (for saving to file)."""
        return {
            "title":self.title,
            "description":self.description,
            "priority":self.priority,
            "category":self.category,
            "done":self.done,
            "created_at":self.created_at,
            "completed_at":self.completed_at,
        }
    

    # ----------------------------------------------------------
    # CONCEPT: Class method (alternative constructor)
    # @classmethod lets us create a Task FROM a dictionary.
    # Useful when we LOAD saved tasks from a file.
    # 'cls' means "the class itself" (like 'self' but for the class).
    # ----------------------------------------------------------

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from a dictionary (for loading from file)."""
        task=cls(
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            category=data["category"],
        )
        task.done=data["done"]
        task.created_at=data["created_at"]
        task.completed_at=data["completed_at"]
        return task
    

    # ----------------------------------------------------------
    # CONCEPT: __str__
    # When you print(task), Python calls this method.
    # Without it, you'd see something ugly like <Task object at 0x...>
    # f-strings (f"...") let you embed variables directly in text.
    # ----------------------------------------------------------

    def __str__(self):
        status="Done" if self.done else "Pending"
        priority_icons = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        icon=priority_icons.get(self.priority, "⚪")
        return(
            f"{icon} [{status}] {self.title}\n"
            f"Category: {self.category}\n"
            f"Note: {self.description or 'No description'}\n"
            f"Created: {self.created_at}"
        )