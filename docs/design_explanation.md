# Smart Study Planner — Design Pattern Explanation

> **Course:** Software Design Patterns  
> **Project:** Smart Study Planner (AI-Style Study Organizer) — v2 (CLI + GUI)

This document explains each design pattern used in the project, why it was chosen, how it is implemented, and how it maps to the theory taught in the course.

---

## 1. Singleton Pattern

### 📌 Theory
> "Ensure a class has only one instance and provide a global point of access to it."
> — GoF, *Design Patterns* (Creational)

A **Singleton** is needed when exactly one object must coordinate actions across the system.

### 🏗️ Where it is used
| Element | File |
|---|---|
| **StudyPlanner** | `scheduler/planner.py` |

### 🔍 How it works

```python
class StudyPlanner(Subject):
    _instance = None               # The one instance, stored at class level

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)   # create only once
            cls._instance._initialized = False
        return cls._instance       # always return the same object

    @classmethod
    def get_instance(cls):         # public accessor
        if cls._instance is None:
            cls()
        return cls._instance
```

### ✅ Why Singleton fits here
- The planner holds the master task list. Two planners with different task lists would cause data inconsistency.
- Every module (CLI, GUI, tests, future API) calls `StudyPlanner.get_instance()` and receives the **same object** with the same state. This is why adding a Tkinter GUI required **zero changes** to the planner.

### ⚡ SOLID Connection
- **Single Responsibility**: the planner manages tasks; the Singleton mechanism is separated into `__new__` + `get_instance`.

---

## 2. Strategy Pattern

### 📌 Theory
> "Define a family of algorithms, encapsulate each one, and make them interchangeable."
> — GoF, *Design Patterns* (Behavioural)

Strategy lets you switch algorithms at runtime without modifying the client.

### 🏗️ Where it is used
| Element | File |
|---|---|
| Abstract Strategy: **SortStrategy** | `patterns/strategy.py` |
| Concrete: **SortByPriority** | `patterns/strategy.py` |
| Concrete: **SortByDeadline** | `patterns/strategy.py` |
| Concrete: **SortByDuration** | `patterns/strategy.py` |
| Context: **StudyPlanner** | `scheduler/planner.py` |

### 🔍 How it works

```
                ┌─────────────────────┐
                │    SortStrategy     │  << abstract >>
                │  + sort(tasks)      │
                └─────────────────────┘
                         △
          ┌──────────────┼──────────────┐
          │              │              │
  SortByPriority  SortByDeadline  SortByDuration

StudyPlanner (context)
  _strategy: SortStrategy      ← reference to current strategy
  set_strategy(s)              ← swap at runtime
  get_schedule() → _strategy.sort(tasks)
```

### ✅ Why Strategy fits here
Different students have different priorities at different times:
- Night before exam → **Sort by Deadline**
- Normal study day  → **Sort by Priority**
- Getting started   → **Sort by Duration** (quick wins first)

The planner's core logic never changes — only the strategy object is swapped.

### ⚡ SOLID Connection
- **Open/Closed**: adding a new strategy (e.g., `SortBySubject`) requires zero changes to existing classes.
- **Single Responsibility**: each strategy class does exactly one thing.

---

## 3. Observer Pattern

### 📌 Theory
> "Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically."
> — GoF, *Design Patterns* (Behavioural)

### 🏗️ Where it is used
| Element | File |
|---|---|
| Abstract Observer: **Observer** | `patterns/observer.py` |
| Abstract Subject:  **Subject** | `patterns/observer.py` |
| Concrete: **ConsoleNotifier** | `patterns/observer.py` |
| Concrete: **DeadlineWatcher** | `patterns/observer.py` |
| Concrete: **LogNotifier** | `patterns/observer.py` |
| Concrete: **GUINotifier** *(new)* | `ui/gui_app.py` |
| Subject (concrete): **StudyPlanner** | `scheduler/planner.py` |

### 🔍 How it works

```
StudyPlanner (Subject)              Observers
  _observers: List[Observer]
  notify_observers(event, task) ──► ConsoleNotifier.update()   (prints to terminal)
                                ──► DeadlineWatcher.update()   (deadline proximity alert)
                                ──► LogNotifier.update()       (writes to event log)
                                ──► GUINotifier.update()       (updates GUI status bar)
```

Every `add_task`, `edit_task`, `delete_task`, and `update_status` call ends with `self.notify_observers(...)`.  Observers decide independently how to react:

| Observer | Where defined | What it does |
|---|---|---|
| `ConsoleNotifier` | `patterns/observer.py` | Prints coloured message to terminal |
| `DeadlineWatcher` | `patterns/observer.py` | Warns when deadline is within 48 h |
| `LogNotifier` | `patterns/observer.py` | Appends timestamped entry to in-memory log |
| `GUINotifier` | `ui/gui_app.py` | Updates the Tkinter status bar live |

> **Open/Closed in action:** `GUINotifier` was added for the GUI mode without touching any existing observer class or the planner. It simply implements the `Observer` interface.

### ✅ Why Observer fits here
When a task changes, multiple independent subsystems need to react (UI, logger, alarm). Observer decouples them completely — the planner doesn't know or care who is listening.

### ⚡ SOLID Connection
- **Open/Closed**: add a new observer (e.g., `EmailNotifier`) by creating one new class, zero existing changes.
- **Dependency Inversion**: the planner depends on the abstract `Observer`, not any concrete notifier.

---

## 4. Factory Method Pattern

### 📌 Theory
> "Define an interface for creating an object, but let subclasses decide which class to instantiate."
> — GoF, *Design Patterns* (Creational)

### 🏗️ Where it is used
| Element | File |
|---|---|
| Creator: **TaskFactory** | `patterns/factory.py` |
| Abstract Product: **Task** | `models/task.py` |
| Concrete Products: **StudyTask, ExamTask, BreakTask** | `models/task.py` |

### 🔍 How it works

```python
# Without Factory (bad – tightly coupled):
task = StudyTask("Revision", 2, deadline, 1.5, subject="Math")

# With Factory (decoupled – planner only knows TaskType):
task = TaskFactory.create(TaskType.STUDY, "Revision", 2, deadline, 1.5, subject="Math")
```

The factory uses a **registry dictionary** that maps each `TaskType` enum to its concrete class:
```python
_registry = {
    TaskType.STUDY: StudyTask,
    TaskType.EXAM:  ExamTask,
    TaskType.BREAK: BreakTask,
}
```

Adding `TaskType.PROJECT → ProjectTask` requires **one line in the registry** — nothing else changes.

### ✅ Why Factory fits here
The planner and CLI should never construct task objects directly. Centralising creation in the factory means:
- Validation in one place
- Easy to extend task types
- Tests can mock the factory

### ⚡ SOLID Connection
- **Open/Closed**: new task types → extend registry, not modify callers.
- **Dependency Inversion**: high-level modules depend on the abstract `Task`, not concrete subclasses.

---

## 5. Adapter Pattern

### 📌 Theory
> "Convert the interface of a class into another interface clients expect. Adapter lets classes work together that could not otherwise."
> — GoF, *Design Patterns* (Structural)

### 🏗️ Where it is used
| Element | File |
|---|---|
| Adaptee: **CalendarSystem** | `patterns/adapter.py` |
| Adapter: **TaskImportAdapter** | `patterns/adapter.py` |
| Client: **StudyPlanner** (via CLI and GUI) | `scheduler/planner.py` |

### 🔍 How it works

```
CalendarSystem.fetch_events()        TaskImportAdapter.get_tasks()
──────────────────────────           ─────────────────────────────
[{                                   [Task, Task, Task, …]
  "name": "Physics Exam",   ──────►  (ready for planner)
  "due": "2026-05-15 09:00",
  "hours": 3.0,
  "importance": 1,
  "type": "Exam",
  "extra_detail": "Physics 301"
}]
```

The adapter:
1. Calls `calendar.fetch_events()` (the Adaptee's incompatible method).
2. Translates key names (`"name"` → `title`, `"importance"` → `priority`, etc.).
3. Converts types (`str` date → `datetime`).
4. Delegates object construction to `TaskFactory`.
5. Returns `List[Task]` — the interface the planner expects.

### ✅ Why Adapter fits here
Real systems must integrate with external data sources (Google Calendar, university APIs, CSV imports). Those sources use their own schemas. The Adapter pattern provides a clean integration seam without modifying either the external class or the planner.

---

## Pattern Interaction Summary

```
main.py  (mode selector)
  ├── ui/cli.py       (CLI presentation only)
  └── ui/gui_app.py  (GUI presentation only — adds GUINotifier observer)
        │
        └── Both share the same backend:
              scheduler/planner.py  ← SINGLETON + OBSERVER Subject + STRATEGY Context
                ├── patterns/strategy.py  ← STRATEGY (3 concrete algorithms)
                ├── patterns/observer.py  ← OBSERVER (3+1 concrete observers)
                ├── patterns/factory.py   ← FACTORY METHOD
                │     └── models/task.py  ← abstract + concrete products
                └── patterns/adapter.py  ← ADAPTER (wraps CalendarSystem)
```

All five patterns collaborate seamlessly, each playing a distinct role with zero overlap of responsibility — a clean demonstration of how patterns are **composable**.

The dual-mode architecture also illustrates a key software engineering principle:
> **Separate presentation from business logic.** The same planner, factory, strategies, and observers work identically whether the user is typing in a terminal or clicking buttons in a window.
