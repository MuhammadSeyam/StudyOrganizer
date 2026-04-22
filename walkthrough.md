# Smart Study Planner — Project Walkthrough

> **Course:** Software Design Patterns  
> **Language:** Python 3.8+ (standard library only — no pip install needed)  
> **Status:** ✅ Complete — all 27 automated tests pass

---

## What Was Built

A fully working command-line study organiser that clearly demonstrates **5 design patterns** through a realistic, cohesive use-case.

---

## Project Structure

```
SmartStudyPlanner/
├── main.py                    ← Entry point  →  python main.py
├── test_all.py                ← Automated tests  →  python test_all.py
│
├── models/
│   └── task.py                ← Task (base) + StudyTask, ExamTask, BreakTask
│
├── patterns/
│   ├── factory.py             ← Factory Method  (TaskFactory)
│   ├── strategy.py            ← Strategy        (SortByPriority/Deadline/Duration)
│   ├── observer.py            ← Observer        (ConsoleNotifier, DeadlineWatcher, LogNotifier)
│   └── adapter.py             ← Adapter         (TaskImportAdapter ↔ CalendarSystem)
│
├── scheduler/
│   └── planner.py             ← Singleton + Observer Subject + Strategy Context
│
├── ui/
│   └── cli.py                 ← Interactive menu (presentation only)
│
└── docs/
    ├── design_explanation.md  ← Theory + code for all 5 patterns
    ├── beginner_guide.md      ← Step-by-step setup & usage guide
    └── demo_output.md         ← Annotated terminal session example
```

---

## Design Patterns — Quick Reference

| # | Pattern | Category | Key Class(es) | File |
|---|---|---|---|---|
| 1 | **Singleton** | Creational | `StudyPlanner` | `scheduler/planner.py` |
| 2 | **Factory Method** | Creational | `TaskFactory` | `patterns/factory.py` |
| 3 | **Strategy** | Behavioural | `SortByPriority`, `SortByDeadline`, `SortByDuration` | `patterns/strategy.py` |
| 4 | **Observer** | Behavioural | `ConsoleNotifier`, `DeadlineWatcher`, `LogNotifier` | `patterns/observer.py` |
| 5 | **Adapter** | Structural | `TaskImportAdapter` wraps `CalendarSystem` | `patterns/adapter.py` |

---

## How Patterns Interact

```
main.py
  └── ui/cli.py                     presentation layer only
        └── StudyPlanner             ← SINGLETON (one global instance)
              │                      ← OBSERVER Subject (notifies all watchers)
              │                      ← STRATEGY Context (delegates sort logic)
              │
              ├── patterns/strategy.py   3 interchangeable sort algorithms
              ├── patterns/observer.py   3 independent notification listeners
              ├── patterns/factory.py    centralised task object creation
              │     └── models/task.py   abstract Task + 3 concrete types
              └── patterns/adapter.py    bridges incompatible CalendarSystem
```

---

## Functional Features

| Feature | Menu Option | Pattern(s) Involved |
|---|---|---|
| Add task (Study / Exam / Break) | `[2]` | Factory Method |
| Edit task fields | `[3]` | Observer |
| Delete task | `[4]` | Observer |
| Update status (Pending/In Progress/Done) | `[5]` | Observer |
| View sorted schedule | `[1]` | Singleton, Strategy |
| Switch sort algorithm live | `[6]` | Strategy |
| Import tasks from calendar | `[7]` | Adapter, Factory |
| See overdue tasks | `[8]` | — |
| View full event log | `[9]` | Observer (LogNotifier) |

---

## Test Results

```
=======================================================
  Smart Study Planner — Automated Test Suite
=======================================================

[1] SINGLETON PATTERN
  ✅ get_instance() always returns the same object
  ✅ Instance is a StudyPlanner

[2] FACTORY METHOD PATTERN
  ✅ Factory creates ExamTask correctly
  ✅ Factory creates StudyTask correctly
  ✅ Factory creates BreakTask correctly
  ✅ ExamTask has 'course' attribute
  ✅ StudyTask has 'subject' attribute
  ✅ BreakTask has 'activity' attribute
  ✅ Planner holds exactly 3 tasks

[3] STRATEGY PATTERN
  ✅ SortByDeadline: first = #3 'Coffee Break'
  ✅ SortByDuration: first = #3 'Coffee Break' (0.5h)
  ✅ SortByPriority: first = #1 'Final Exam Prep' (priority 1)
  ✅ Strategy name reported correctly

[4] OBSERVER PATTERN
  ✅ update_status() changes task status correctly
  ✅ LogNotifier captured the status-change event
  ✅ edit_task() updates title
  ✅ LogNotifier captured the edit event
  ✅ remove_observer() stops notifications correctly

[5] ADAPTER PATTERN
  ✅ Adapter imports exactly 3 tasks from CalendarSystem
  ✅ First imported task is ExamTask
  ✅ Second imported task is StudyTask
  ✅ Third imported task is BreakTask
  ✅ Adapter converted deadline correctly for 'Physics Exam Prep'
  ✅ Adapter converted deadline correctly for 'Read Chapter 7 – Networks'
  ✅ Adapter converted deadline correctly for 'Afternoon Break'
  ✅ Planner now holds 6 tasks (3 original + 3 imported)

[6] DELETE
  ✅ delete_task() returns True on success
  ✅ Deleted task is gone from planner
  ✅ Planner has 5 tasks after deletion

=======================================================
  All 27 tests passed! Project is fully functional.
=======================================================
```

---

## How to Run

```bash
# 1. Open terminal and navigate to project folder
cd "d:\Academic\My Courses\Year 3\Semester 2\Software design patterns\Project\SmartStudyPlanner"

# 2. Run the interactive app
python main.py

# 3. (Optional) Run automated tests
python test_all.py
```

> **No installation required** — uses Python standard library only.

---

## Documentation Delivered

| File | Purpose |
|---|---|
| `docs/design_explanation.md` | Full GoF theory + code snippets for all 5 patterns |
| `docs/beginner_guide.md` | Step-by-step setup, feature walkthrough, test scenarios |
| `docs/demo_output.md` | Full annotated terminal session showing each pattern live |
| `README.md` | Project overview, quick start, architecture diagram |
