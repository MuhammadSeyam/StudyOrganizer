# Smart Study Planner — Beginner's Guide

> 🎓 **For students with basic Python knowledge.  
> No prior experience with design patterns required to run this project.**

---

## What is this project?

The **Smart Study Planner** is a command-line Python application that helps you organise your study tasks by priority, deadline, or duration. Under the hood it demonstrates **five software design patterns** from your course.

---

## Prerequisites

You need **Python 3.8 or later** installed.

### Check your Python version
Open a terminal (Command Prompt / PowerShell on Windows, or Terminal on Mac/Linux) and type:

```bash
python --version
```

You should see something like `Python 3.10.x`. If you see an error, download Python from [python.org](https://python.org).

> ✅ **Good news:** This project uses **only Python's standard library** — no `pip install` needed!

---

## Project Structure

```
SmartStudyPlanner/
│
├── main.py                   ← START HERE — run this file
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
│   └── planner.py            ← Singleton + core logic
│
├── ui/
│   └── cli.py                ← Interactive menu
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
# Replace the path with where you saved the project
cd "d:\Academic\My Courses\Year 3\Semester 2\Software design patterns\Project\SmartStudyPlanner"
```

### Step 3 — Run the Application

```bash
python main.py
```

You should see the welcome banner and main menu:

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

---

## How to Use Each Feature

### 📋 [1] View Schedule
Shows all tasks sorted by the active strategy.  
Default is **Sort by Priority** (most important first).

---

### ➕ [2] Add Task
Walk-through:

1. Choose task type:  `1` = Study, `2` = Exam, `3` = Break
2. Enter a title:  e.g. `Revise Algorithms Chapter 4`
3. Enter priority: `1` = most urgent, `5` = least urgent
4. Enter deadline: format is `YYYY-MM-DD HH:MM`  
   Example: `2026-05-20 14:00`
5. Enter duration in hours: e.g. `2.5`
6. Enter the type-specific field (subject / course / activity)

**Example session:**
```
Task Types:
  1 Study Task
  2 Exam Task
  3 Break Task
Choose type [1-3]: 1
Title: Revise Algorithms Chapter 4
Priority [1=High … 5=Low]: 2
Deadline [YYYY-MM-DD HH:MM]: 2026-05-20 14:00
Estimated Duration (hours): 2.5
Subject (e.g. Math, Physics): CS301

  🔔 [NOTIFICATION] Task added → Task #1 'Revise Algorithms Chapter 4'
  ✅ Task #1 'Revise Algorithms Chapter 4' added successfully.
```

---

### ✏️ [3] Edit Task
Enter the Task ID (shown in the schedule view).  
Press **ENTER** to keep any field unchanged.

---

### 🗑️ [4] Delete Task
Enter the Task ID, then confirm with `y`.

---

### 🔄 [5] Update Task Status
Choose a task ID, then:
- `1` → Pending  
- `2` → In Progress  
- `3` → Done  

The planner automatically notifies all observers.

---

### 🔀 [6] Change Scheduling Strategy
Swap the sort algorithm live — no restart needed:
- `1` → By Priority (default)
- `2` → By Deadline  
- `3` → By Duration  

Switch to **By Deadline** the night before exams!

---

### 📥 [7] Import from Calendar (Adapter Demo)
Imports 3 pre-defined tasks from the simulated `CalendarSystem`.  
This demonstrates the **Adapter Pattern** — no setup needed.

---

### ⚠️ [8] Show Overdue Tasks
Lists any task whose deadline has passed and is not marked Done.

---

### 📜 [9] Show Event Log
Displays every event recorded by the `LogNotifier` observer since startup, with timestamps.

---

## Testing Features Step-by-Step

Here is a complete testing script you can follow:

### Test 1 — Add three tasks
```
Press 2 → Add a Study task   (priority 2, deadline 2026-05-18 09:00, 1.5h)
Press 2 → Add an Exam task   (priority 1, deadline 2026-05-20 09:00, 3.0h)
Press 2 → Add a Break task   (priority 4, deadline 2026-05-18 15:00, 0.5h)
```

### Test 2 — View schedule (By Priority)
```
Press 1 → Exam task appears first (priority 1)
```

### Test 3 — Switch strategy to Deadline
```
Press 6 → Choose 2
Press 1 → Study task appears first (earlier deadline)
```

### Test 4 — Switch strategy to Duration
```
Press 6 → Choose 3
Press 1 → Break task appears first (0.5h shortest)
```

### Test 5 — Update status
```
Press 5 → Enter the Exam task ID → Choose 2 (In Progress)
Press 1 → Confirm the 🔄 icon appears
```

### Test 6 — Import from Calendar
```
Press 7 → 3 tasks are imported; observe notifications
Press 1 → Schedule now shows 6 tasks
```

### Test 7 — View Event Log
```
Press 9 → See timestamped list of every action taken
```

### Test 8 — Delete a task
```
Press 4 → Enter any task ID → Confirm with y
Press 1 → Task is gone from schedule
```

---

## Common Problems & Solutions

| Problem | Solution |
|---|---|
| `python: command not found` | Use `python3 main.py` instead |
| `ModuleNotFoundError` | Make sure you are running from the `SmartStudyPlanner/` folder |
| `Invalid date format` | Use exactly `YYYY-MM-DD HH:MM`, e.g. `2026-05-15 09:00` |
| Colours don't show (Windows CMD) | Use PowerShell or Windows Terminal — they support ANSI colours |

---

## Stopping the Application

- Type `0` and press Enter to exit cleanly.
- Or press `Ctrl + C` at any time.

---

## Example Scenario: Finals Week

You have finals week coming up. Here is how you'd use the planner:

1. **Add** your exam tasks with priority `1`, deadlines matching your exam schedule.
2. **Add** your study sessions as Study tasks with priority `2`.
3. **Add** break tasks with priority `4` for mental rest.
4. **Set strategy to Deadline** — now you always see what needs attention first.
5. As you finish tasks, **update status to Done** to keep the list clean.
6. Check **Overdue Tasks** daily to catch anything slipping.
7. Review the **Event Log** to see a history of everything you've done.
