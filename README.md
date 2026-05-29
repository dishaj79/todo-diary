# 📔 ToDo Diary — Python CLI Task Manager

A command-line **To-Do List & Diary app** built with pure Python. Tasks persist between sessions via JSON, and the code is structured using Object-Oriented Programming principles.

> Built as a hands-on Python learning project — covering OOP, file I/O, JSON, list comprehensions, error handling, and unit testing.

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add tasks | With title, description, priority, and category |
| ✅ Complete tasks | Mark tasks done with a timestamp |
| 🗑️ Delete tasks | Remove individual tasks or clear all done tasks |
| 🔍 Search | Find tasks by keyword across title and description |
| 🔎 Filter | Filter by category or priority |
| 📊 Stats | See completion percentage at a glance |
| 💾 Persistent | Tasks auto-save to `data/tasks.json` |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher

### Run the app
```bash
# Clone the repository
git clone https://github.com/dishaj79/todo-diary.git

# Run directly — no dependencies needed!
python main.py
```

### Run the tests
```bash
python -m pytest tests/ -v
# or
python -m unittest discover
```

---

## 📁 Project Structure

```
todo-diary/
├── main.py          # Entry point — interactive menu loop
├── task.py          # Task class (OOP data model)
├── diary.py         # Diary class (business logic + file I/O)
├── tests/
│   └── test_tasks.py  # Unit tests (15 test cases)
├── data/
│   └── tasks.json   # Auto-generated — your saved tasks
└── README.md
```

---

## 📸 Demo

```
╔══════════════════════════════════════╗
║     📔  TODO DIARY  —  MAIN MENU     ║
╠══════════════════════════════════════╣
║  1. ➕  Add a task                   ║
║  2. 📋  View all tasks               ║
║  3. ✅  Mark task as done            ║
...
```

---
