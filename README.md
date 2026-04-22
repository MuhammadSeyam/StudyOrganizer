# 🎓 Smart Study Planner
### AI-Style Study Organizer — Software Design Patterns Project

> A clean, well-structured Python CLI application demonstrating **5 core design patterns** from the Software Design Patterns course.

---

## 📐 Design Patterns Implemented

| # | Pattern | Category | Where Used |
|---|---|---|---|
| 1 | **Singleton** | Creational | `StudyPlanner` — one instance for the entire session |
| 2 | **Factory Method** | Creational | `TaskFactory` — creates `StudyTask`, `ExamTask`, `BreakTask` |
| 3 | **Strategy** | Behavioural | `SortByPriority`, `SortByDeadline`, `SortByDuration` |
| 4 | **Observer** | Behavioural | `ConsoleNotifier`, `DeadlineWatcher`, `LogNotifier` |
| 5 | **Adapter** | Structural | `TaskImportAdapter` wraps `CalendarSystem` |

---

## 🚀 Quick Start

```bash
# Navigate to project folder
cd SmartStudyPlanner

# Run (no install needed — standard library only)
python main.py
```

---

## 📁 Project Structure

```
SmartStudyPlanner/
├── main.py                   ← Entry point
├── models/
│   └── task.py               ← Task, StudyTask, ExamTask, BreakTask
├── patterns/
│   ├── observer.py           ← Observer pattern
│   ├── strategy.py           ← Strategy pattern
│   ├── factory.py            ← Factory Method pattern
│   └── adapter.py            ← Adapter pattern
├── scheduler/
│   └── planner.py            ← Singleton + context for all patterns
├── ui/
│   └── cli.py                ← Interactive CLI menu
└── docs/
    ├── design_explanation.md ← Pattern theory & code walkthrough
    ├── beginner_guide.md     ← Step-by-step setup and usage guide
    └── demo_output.md        ← Annotated example terminal session
```

---

## ⚙️ Requirements

- Python 3.8+
- No external libraries required

---

## 📋 Features

- ✅ Add / Edit / Delete tasks
- ✅ Three task types: Study, Exam, Break
- ✅ Three sort strategies (switchable at runtime)
- ✅ Real-time observer notifications
- ✅ Deadline proximity warnings
- ✅ Full event log with timestamps
- ✅ External calendar import (Adapter demo)
- ✅ Overdue task detection

---

## 📂 Documentation

| File | Description |
|---|---|
| `docs/design_explanation.md` | Full explanation of each pattern with code and theory |
| `docs/beginner_guide.md` | Step-by-step guide for first-time users |
| `docs/demo_output.md` | Annotated example terminal session |

---

## 🏗️ Architecture Overview

```
main.py
  └── ui/cli.py                    (presentation layer)
        └── scheduler/planner.py   (SINGLETON + OBSERVER Subject + STRATEGY Context)
              ├── patterns/strategy.py   (3 sort algorithms)
              ├── patterns/observer.py   (3 notification listeners)
              ├── patterns/factory.py    (task creation)
              │     └── models/task.py   (Task hierarchy)
              └── patterns/adapter.py    (CalendarSystem bridge)
```

---

*Course: Software Design Patterns | Project: Smart Study Planner*
