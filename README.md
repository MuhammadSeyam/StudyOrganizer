# 🎓 Smart Study Planner
### AI-Style Study Organizer — Software Design Patterns Project

> A clean, well-structured Python application demonstrating **5 core design patterns** with **dual-mode support** (CLI + GUI).

---

## 📐 Design Patterns Implemented

| # | Pattern | Category | Where Used |
|---|---|---|---|
| 1 | **Singleton** | Creational | `StudyPlanner` — one instance shared by CLI and GUI |
| 2 | **Factory Method** | Creational | `TaskFactory` — creates `StudyTask`, `ExamTask`, `BreakTask` |
| 3 | **Strategy** | Behavioural | `SortByPriority`, `SortByDeadline`, `SortByDuration` |
| 4 | **Observer** | Behavioural | `ConsoleNotifier`, `DeadlineWatcher`, `LogNotifier`, `GUINotifier` |
| 5 | **Adapter** | Structural | `TaskImportAdapter` wraps `CalendarSystem` |

---

## 🚀 Quick Start

```bash
# Navigate to project folder
cd SmartStudyPlanner

# Run (no install needed — standard library + Tkinter only)
python main.py
```

At startup you will be asked to choose a mode:
```
Select Application Mode:
  1  →  CLI  (Terminal interface)
  2  →  GUI  (Tkinter window)
```

---

## 📁 Project Structure

```
SmartStudyPlanner/
├── main.py                   ← Launcher: choose CLI [1] or GUI [2]
├── test_all.py               ← 27 automated backend tests
├── test_gui.py               ← 18 headless GUI layer tests
│
├── models/
│   └── task.py               ← Task, StudyTask, ExamTask, BreakTask
│
├── patterns/
│   ├── observer.py           ← Observer pattern (Subject + 4 observers)
│   ├── strategy.py           ← Strategy pattern (3 sort algorithms)
│   ├── factory.py            ← Factory Method pattern
│   └── adapter.py            ← Adapter pattern
│
├── scheduler/
│   └── planner.py            ← Singleton + Strategy Context + Observer Subject
│
├── ui/
│   ├── cli.py                ← CLI mode: interactive terminal menu
│   └── gui_app.py            ← GUI mode: dark-themed Tkinter window
│
└── docs/
    ├── design_explanation.md ← Pattern theory & code walkthrough
    ├── beginner_guide.md     ← Step-by-step setup and usage guide
    └── demo_output.md        ← Annotated example session (both modes)
```

---

## ⚙️ Requirements

- Python 3.8+
- Tkinter (included with all standard Python installers on Windows/macOS)
- No `pip install` required

> **Linux users:** if Tkinter is missing, run `sudo apt install python3-tk`

---

## 📋 Features

| Feature | CLI | GUI |
|---|:---:|:---:|
| Add / Edit / Delete tasks | ✅ | ✅ |
| Three task types (Study, Exam, Break) | ✅ | ✅ |
| Three sort strategies (switchable live) | ✅ | ✅ |
| Real-time observer notifications | ✅ | ✅ |
| Deadline proximity warnings | ✅ | ✅ |
| Full event log with timestamps | ✅ | ✅ |
| External calendar import (Adapter demo) | ✅ | ✅ |
| Overdue task detection | ✅ | ✅ |
| Status bar showing last notification | — | ✅ |
| Colour-coded task rows by status | — | ✅ |

---

## 🏗️ Architecture Overview

```
main.py  (mode selector)
  ├── mode 1 → ui/cli.py       (terminal presentation)
  └── mode 2 → ui/gui_app.py   (Tkinter presentation)
                    │
                    └── Both call the SAME backend:
                          StudyPlanner.get_instance()   [SINGLETON]
                            ├── patterns/strategy.py    [STRATEGY]
                            ├── patterns/observer.py    [OBSERVER]
                            ├── patterns/factory.py     [FACTORY METHOD]
                            │     └── models/task.py
                            └── patterns/adapter.py     [ADAPTER]
```

**Key principle:** CLI and GUI are pure presentation layers. Zero business logic lives in either UI file. Swapping or adding a third interface (e.g., web API) requires no changes to the backend.

---

## 📂 Documentation

| File | Description |
|---|---|
| `docs/design_explanation.md` | Full GoF theory + code for all 5 patterns + GUINotifier |
| `docs/beginner_guide.md` | Step-by-step guide for CLI and GUI modes |
| `docs/demo_output.md` | Annotated example sessions for both modes |

---

## 🧪 Running Tests

```bash
python test_all.py   # 27 backend tests  (all patterns)
python test_gui.py   # 18 GUI layer tests (headless, no window)
```

---

*Course: Software Design Patterns | Project: Smart Study Planner v2*
