# ============================================================
#  main.py  —  Entry point (run this file!)
# ============================================================
#
#  CONCEPTS covered here:
#  - while loops (keep running until user quits)
#  - input()  (get text from the user)
#  - if / elif / else  (decision making)
#  - Functions  (breaking code into reusable chunks)
#  - The  if __name__ == "__main__"  pattern
# ============================================================


from diary import Diary

# ── HELPER: Print the menu ─────────────────────────────────
 
def print_menu():
    print("""
╔══════════════════════════════════════╗
║     📔  TODO DIARY  —  MAIN MENU     ║
╠══════════════════════════════════════╣
║  1. ➕  Add a task                   ║
║  2. 📋  View all tasks               ║
║  3. ✅  Mark task as done            ║
║  4. 🔄  Mark task as pending         ║
║  5. 🗑️   Delete a task               ║
║  6. 🔍  Search tasks                 ║
║  7. 📊  Show stats                   ║
║  8. 🧹  Clear completed tasks        ║
║  9. 🔎  Filter by category/priority  ║
║  0. 🚪  Quit                         ║
╚══════════════════════════════════════╝
    """)


# ── HELPER: Ask for input, with an optional default ────────
#
# CONCEPT: Functions with default parameters
# If the caller doesn't pass 'default', it stays None.
 
def ask(prompt, default=None):
    """Show a prompt and return the user's input. Strips extra spaces."""
    value = input(f"  {prompt}: ").strip()
    # CONCEPT: 'or' — if value is empty (""), use the default instead
    return value or default


# ── MAIN LOOP ──────────────────────────────────────────────
 
def main():
    print("\n🌟 Welcome to your ToDo Diary!\n")
    diary = Diary()   # Creates a Diary object (loads saved tasks automatically)
 
    # CONCEPT: while True — runs forever until we explicitly 'break'
    while True:
        print_menu()
 
        # input() pauses and waits for the user to type something
        choice = input("  Enter your choice: ").strip()
    
        # ── 1. ADD ────────────────────────────────────────
        if choice == "1":
            print("\n── Add New Task ──")
            title = ask("Task title (required)")
 
            # CONCEPT: Validation loop
            # Keep asking until the user gives us something
            if not title:
                print("  ⚠️  Title cannot be empty!")
                continue   # 'continue' skips the rest of this loop iteration
 
            desc     = ask("Description (press Enter to skip)", default="")
            priority = ask("Priority [low / medium / high] (default: medium)", default="medium")
            category = ask("Category  [work / personal / study / ...] (default: general)", default="general")
 
            diary.add_task(title, desc, priority, category)

        # ── 2. VIEW ───────────────────────────────────────
        elif choice == "2":
            diary.list_tasks()
        
        # ── 3. MARK DONE ──────────────────────────────────
        elif choice == "3":
            diary.list_tasks(show="pending")
            num = ask("Enter task number to mark done")
            diary.complete_task(num)

        # ── 4. MARK PENDING ───────────────────────────────
        elif choice == "4":
            diary.list_tasks(show="done")
            num = ask("Enter task number to mark pending")
            diary.undo_task(num)
        
        # ── 5. DELETE ─────────────────────────────────────
        elif choice == "5":
            diary.list_tasks()
            num = ask("Enter task number to delete")
 
            # CONCEPT: Confirmation prompt — avoid accidental deletes
            confirm = input("  ❓ Are you sure? (y/n): ").strip().lower()
            if confirm == "y":
                diary.delete_task(num)
            else:
                print("  ↩️  Cancelled.")
 
        # ── 6. SEARCH ─────────────────────────────────────
        elif choice == "6":
            keyword = ask("Search keyword")
            if keyword:
                diary.search(keyword)
 
        # ── 7. STATS ──────────────────────────────────────
        elif choice == "7":
            diary.show_stats()
 
        # ── 8. CLEAR DONE ─────────────────────────────────
        elif choice == "8":
            confirm = input("  ❓ Remove ALL completed tasks? (y/n): ").strip().lower()
            if confirm == "y":
                diary.clear_done()
 
        # ── 9. FILTER ─────────────────────────────────────
        elif choice == "9":
            print("\n── Filter Tasks ──")
            print("  Leave blank to skip that filter.")
            cat  = ask("Category (e.g. work, personal)", default=None)
            pri  = ask("Priority (low / medium / high)",  default=None)
            diary.list_tasks(category=cat, priority=pri)
 
        # ── 0. QUIT ───────────────────────────────────────
        elif choice == "0":
            print("\n👋 Goodbye! Keep being productive. 🚀\n")
            break   # 'break' exits the while loop entirely
 
        else:
            print("  ⚠️  Invalid choice. Please enter a number from the menu.")
 
 
# ============================================================
#  CONCEPT: if __name__ == "__main__"
#
#  When Python runs a file directly, it sets __name__ = "__main__"
#  When a file is IMPORTED by another file, __name__ = the file's name.
#
#  This pattern means: "Only run main() if this file is run directly,
#  NOT if it's imported as a module."
#  It's a Python best practice — always use it for your entry points!
# ============================================================
if __name__ == "__main__":
    main()