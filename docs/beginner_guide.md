# Smart Study Planner — Beginner's Guide

> 🎓 **For students with basic Python knowledge.  
> No prior experience with design patterns required to run this project.**

---

## What is this project?

The **Smart Study Planner** is a Python application that helps you organise your study tasks by priority, deadline, or duration. It supports **two interfaces** — a terminal menu (CLI) and a graphical window (GUI) — both powered by the same backend. Under the hood it demonstrates **five software design patterns** from your course.

---

## Prerequisites

You need **Python 3.8 or later** installed.

### Check your Python version
Open a terminal (Command Prompt / PowerShell on Windows, or Terminal on Mac/Linux) and type:

```bash
python --version
```

You should see something like `Python 3.10.x`. If you see an error, download Python from [python.org](https://python.org).

> ✅ **Good news:** This project uses **only Python's standard library + Tkinter** — no `pip install` needed!  
> Tkinter is included by default with all Windows and macOS Python installers.  
> Linux users: `sudo apt install python3-tk`

---

## Project Structure

```
SmartStudyPlanner/
│
├── main.py                   ← START HERE — run this file
├── test_all.py               ← Run to verify backend (27 tests)
├── test_gui.py               ← Run to verify GUI layer (18 tests)
│
├── models/
│   └── task.py               ← Defines Task, StudyTask, ExamTask, BreakTask
│
├── patterns/
│   ├── observer.py           ← Observer Pattern (notifications)
│   ├── strategy.py           ← Strategy Pattern (sort algorithms)
│   ├── factory.py            ← Factory Method Pattern (task creation)
│   └── adapter.py            ← Adapter Pattern (external calendar)
│
├── scheduler/
│   └── planner.py            ← Singleton + core logic (shared by CLI and GUI)
│
├── ui/
│   ├── cli.py                ← CLI mode: interactive terminal menu
│   └── gui_app.py            ← GUI mode: dark-themed Tkinter window
│
└── docs/
    ├── design_explanation.md ← Pattern explanations (this subject)
    ├── beginner_guide.md     ← You are reading this
    └── demo_output.md        ← Example run output
```

---

## How to Run the Project

### Step 1 — Open a Terminal
- **Windows**: Press `Win + R`, type `cmd`, press Enter.  
  Or open **PowerShell** from the Start menu.
- **Mac/Linux**: Open **Terminal**.

### Step 2 — Navigate to the Project Folder

```bash
cd "d:\Academic\My Courses\Year 3\Semester 2\Software design patterns\Project\SmartStudyPlanner"
```

### Step 3 — Run the Application

```bash
python main.py
```

You will see a mode-selection prompt:

```
============================================
   Smart Study Planner — Launcher
============================================
  Select Application Mode:
    1  →  CLI  (Terminal interface)
    2  →  GUI  (Tkinter window)
============================================
  Your choice [1/2]:
```

- Type **`1`** and press Enter for the **terminal menu**.
- Type **`2`** and press Enter for the **graphical window**.

---

## Mode 1 — CLI (Terminal)

After choosing `1`, you see the main menu:

```
  🎓 Welcome to Smart Study Planner!
  Observers registered: ConsoleNotifier, DeadlineWatcher, LogNotifier
  Default strategy: Sort by Priority

╔════════════════════════════════════════╗
║     🎓  Smart Study Planner  🎓         ║
╠════════════════════════════════════════╣
  [1] View Schedule
  [2] Add Task
  [3] Edit Task
  [4] Delete Task
  [5] Update Task Status
  [6] Change Scheduling Strategy
  [7] Import from Calendar  (Adapter demo)
  [8] Show Overdue Tasks
  [9] Show Event Log
  [0] Exit
╚════════════════════════════════════════╝
  Choose option:
```

### CLI Feature Guide

#### 📋 [1] View Schedule
Shows all tasks sorted by the active strategy. Default is **Sort by Priority**.

#### ➕ [2] Add Task
Walk-through:
1. Choose task type: `1` = Study, `2` = Exam, `3` = Break
2. Enter a title, e.g. `Revise Algorithms Chapter 4`
3. Enter priority: `1` = most urgent, `5` = least urgent
4. Enter deadline in format `YYYY-MM-DD HH:MM`, e.g. `2026-05-20 14:00`
5. Enter duration in hours, e.g. `2.5`
6. Enter the type-specific field (subject / course / activity)

#### ✏️ [3] Edit Task
Enter the Task ID (shown in the schedule). Press **ENTER** to keep any field unchanged.

#### 🗑️ [4] Delete Task
Enter the Task ID, confirm with `y`.

#### 🔄 [5] Update Task Status
Choose a task ID, then: `1` Pending · `2` In Progress · `3` Done

#### 🔀 [6] Change Scheduling Strategy
- `1` By Priority (default)
- `2` By Deadline — great the night before exams!
- `3` By Duration

#### 📥 [7] Import from Calendar (Adapter Demo)
Imports 3 pre-built tasks from the simulated `CalendarSystem`. Demonstrates the **Adapter Pattern**.

#### ⚠️ [8] Show Overdue Tasks
Lists tasks whose deadline has passed and are not marked Done.

#### 📜 [9] Show Event Log
Shows every event recorded by the `LogNotifier` observer, with timestamps.

#### 🚪 [0] Exit
Type `0` or press `Ctrl + C` at any time.

---

## Mode 2 — GUI (Tkinter Window)

After choosing `2`, a dark-themed window opens with:

| Element | Description |
|---|---|
| **Header** | Title + "Schedule by" dropdown (Strategy pattern) |
| **Toolbar** | Add, Edit, Delete, Update Status, Import Calendar, Event Log |
| **Task table** | Shows all tasks with colour-coded rows by status |
| **Status bar** | Live notifications from the GUINotifier observer |

### GUI Walkthrough

1. **Add a task** — click **＋ Add Task** → fill in the form → click **Add Task**
2. **Edit a task** — select a row → click **✏ Edit Task** (or double-click the row)
3. **Delete a task** — select a row → click **🗑 Delete** → confirm
4. **Change status** — select a row → click **🔄 Update Status** → choose from radio buttons
5. **Switch strategy** — use the **Schedule by** dropdown in the top-right; table re-sorts instantly
6. **Import from calendar** — click **📥 Import Calendar** → 3 tasks are added automatically
7. **View event log** — click **📜 Event Log** → scrollable window shows all recorded events

---

## Testing Features (CLI Quick-Test Script)

| Step | Action | Expected result |
|---|---|---|
| 1 | Add Study (priority 2, deadline 2026-05-18) | Notification: "Task added" |
| 2 | Add Exam (priority 1, deadline 2026-05-20) | Notification: "Task added" |
| 3 | Add Break (priority 4, deadline 2026-05-18) | Notification: "Task added" |
| 4 | View Schedule (By Priority) | Exam appears first |
| 5 | Switch strategy to Deadline | Study appears first |
| 6 | Switch strategy to Duration | Break appears first (0.5h) |
| 7 | Update Exam status to In Progress | Status icon changes |
| 8 | Import from Calendar | 3 more tasks added |
| 9 | View Event Log | All 8 actions timestamped |
| 10 | Delete Break task | Task removed from list |

---

## Common Problems & Solutions

| Problem | Solution |
|---|---|
| `python: command not found` | Use `python3 main.py` instead |
| `ModuleNotFoundError` | Run from the `SmartStudyPlanner/` folder |
| `Invalid date format` | Use exactly `YYYY-MM-DD HH:MM`, e.g. `2026-05-15 09:00` |
| Colours don't show (Windows CMD) | Use PowerShell or Windows Terminal |
| GUI window doesn't open | Check Tkinter: `python -c "import tkinter"` — if it fails, install python3-tk |

---

## Running the Automated Tests

```bash
python test_all.py   # 27 backend tests — verifies all 5 patterns
python test_gui.py   # 18 GUI tests    — verifies GUI wiring (headless)
```

Both should end with **"All tests passed!"**

---

## Example Scenario: Finals Week

1. **Add** exam tasks with priority `1` matching your exam schedule.
2. **Add** study sessions as Study tasks with priority `2`.
3. **Add** break tasks with priority `4` for mental rest.
4. **Set strategy to Deadline** — always see what's due soonest.
5. **Update status to Done** as you complete tasks.
6. **Check Overdue Tasks** daily to catch anything slipping.
7. **Review the Event Log** to see a full history of your planning session.
