# Smart Study Planner — Example Run / Demo Output

This document shows exactly what you will see when you run the application,  
with sample inputs and the corresponding outputs.

---

## Startup

```
$ python main.py

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

## Demo Step 1 — Add Three Tasks

### Input: 2 (Add Task)
```
  ── Add New Task ─────────────────────────────

  Task Types:
    1 Study Task  (subject)
    2 Exam Task   (course)
    3 Break Task  (activity)
  Choose type [1-3]: 2
  Title: Data Structures Final Exam
  Priority [1=High … 5=Low]: 1
  Deadline [YYYY-MM-DD HH:MM]: 2026-05-25 09:00
  Estimated Duration (hours): 4
  Course name: CS201
```
### Output:
```
  🔔 [NOTIFICATION] Task added → Task #1 'Data Structures Final Exam'
  ✅ Task #1 'Data Structures Final Exam' added successfully.
```

### Input: 2 (Add Task again)
```
  Choose type [1-3]: 1
  Title: Revise Sorting Algorithms
  Priority [1=High … 5=Low]: 2
  Deadline [YYYY-MM-DD HH:MM]: 2026-05-22 18:00
  Estimated Duration (hours): 2
  Subject: CS201 – Data Structures
```
### Output:
```
  🔔 [NOTIFICATION] Task added → Task #2 'Revise Sorting Algorithms'
  ✅ Task #2 'Revise Sorting Algorithms' added successfully.
```

### Input: 2 (Add Task again)
```
  Choose type [1-3]: 3
  Title: Coffee Break
  Priority [1=High … 5=Low]: 5
  Deadline [YYYY-MM-DD HH:MM]: 2026-05-22 12:00
  Estimated Duration (hours): 0.5
  Activity: Coffee & stretch
```
### Output:
```
  🔔 [NOTIFICATION] Task added → Task #3 'Coffee Break'
  ✅ Task #3 'Coffee Break' added successfully.
```

---

## Demo Step 2 — View Schedule (By Priority)

### Input: 1
```
  ╔════════════════════════════════════════════════════════════════════════╗
  ║  📅  SMART STUDY PLANNER  –  Sort by Priority (1=Highest)            ║
  ╠════════════════════════════════════════════════════════════════════════╣
  ║   1. 📝 [Exam ] #1   Data Structures Final Exam   ⏳ Pending         ║
  ║      Priority:1  Deadline:2026-05-25 09:00  Duration:4.0h            ║
  ╠────────────────────────────────────────────────────────────────────────╣
  ║   2. 📖 [Study] #2   Revise Sorting Algorithms    ⏳ Pending         ║
  ║      Priority:2  Deadline:2026-05-22 18:00  Duration:2.0h            ║
  ╠────────────────────────────────────────────────────────────────────────╣
  ║   3. ☕ [Break] #3   Coffee Break                 ⏳ Pending         ║
  ║      Priority:5  Deadline:2026-05-22 12:00  Duration:0.5h            ║
  ╚════════════════════════════════════════════════════════════════════════╝
  Total tasks: 3
```

---

## Demo Step 3 — Switch Strategy to Deadline

### Input: 6
```
  ── Change Scheduling Strategy ───────────────
  Current strategy: Sort by Priority (1=Highest)

  1 Sort by Priority  (1 = highest first)
  2 Sort by Deadline  (earliest first)
  3 Sort by Duration  (shortest first)

  Choose strategy [1-3]: 2
```
### Output:
```
  🔔 [NOTIFICATION] Scheduling strategy changed to: Sort by Deadline (Earliest First)
  ✅ Strategy switched to: Sort by Deadline (Earliest First)
```

### Input: 1 (View Schedule)
```
  ╔════════════════════════════════════════════════════════════════════════╗
  ║  📅  SMART STUDY PLANNER  –  Sort by Deadline (Earliest First)       ║
  ╠════════════════════════════════════════════════════════════════════════╣
  ║   1. ☕ [Break] #3   Coffee Break                 ⏳ Pending         ║
  ║      Priority:5  Deadline:2026-05-22 12:00  Duration:0.5h            ║
  ╠────────────────────────────────────────────────────────────────────────╣
  ║   2. 📖 [Study] #2   Revise Sorting Algorithms    ⏳ Pending         ║
  ║      Priority:2  Deadline:2026-05-22 18:00  Duration:2.0h            ║
  ╠────────────────────────────────────────────────────────────────────────╣
  ║   3. 📝 [Exam ] #1   Data Structures Final Exam   ⏳ Pending         ║
  ║      Priority:1  Deadline:2026-05-25 09:00  Duration:4.0h            ║
  ╚════════════════════════════════════════════════════════════════════════╝
  Total tasks: 3
```
> ✅ **Notice**: the order changed completely — now earliest deadline comes first.

---

## Demo Step 4 — Update Task Status

### Input: 5
```
  ── Update Task Status ───────────────────────

  Task ID: 2

  Statuses:
    1 Pending
    2 In Progress
    3 Done

  Choose status [1-3]: 2
```
### Output:
```
  🔔 [NOTIFICATION] Status changed to 'In Progress' → Task #2 'Revise Sorting Algorithms'
  ✅ Status updated.
```

---

## Demo Step 5 — Import from Calendar (Adapter Pattern)

### Input: 7
```
  ── Import from External Calendar (Adapter) ──
  Connecting to CalendarSystem (simulated external source)…
```
### Output:
```
  🔔 [NOTIFICATION] Task imported from external source → Task #4 'Physics Exam Prep'
  🔔 [NOTIFICATION] Task imported from external source → Task #5 'Read Chapter 7 – Networks'
  🔔 [NOTIFICATION] Task imported from external source → Task #6 'Afternoon Break'
  ✅ 3 tasks imported from CalendarSystem.
```

---

## Demo Step 6 — Show Event Log (Observer Output)

### Input: 9
```
  ── Event Log (LogNotifier) ──────────────────

  ── Event Log ──────────────────────────────
  [2026-04-22 14:35:01] | Task #1 – Task added
  [2026-04-22 14:35:22] | Task #2 – Task added
  [2026-04-22 14:35:38] | Task #3 – Task added
  [2026-04-22 14:36:10] – Scheduling strategy changed to: Sort by Deadline (Earliest First)
  [2026-04-22 14:36:45] | Task #2 – Status changed to 'In Progress'
  [2026-04-22 14:37:02] | Task #4 – Task imported from external source
  [2026-04-22 14:37:02] | Task #5 – Task imported from external source
  [2026-04-22 14:37:02] | Task #6 – Task imported from external source
  ───────────────────────────────────────────
```
> ✅ **Note**: Every single action is timestamped and recorded — this is the `LogNotifier` observer at work.

---

## Demo Step 7 — Delete a Task

### Input: 4
```
  ── Delete Task ──────────────────────────────
  Task ID to delete: 3
  Delete 'Coffee Break'? [y/N]: y
```
### Output:
```
  🔔 [NOTIFICATION] Task deleted: 'Coffee Break' → Task #3 'Coffee Break'
  🗑️  Task #3 deleted.
```

---

## Demo Step 8 — Exit

### Input: 0
```
  👋 Goodbye! Stay on schedule!
```

---

## Full Pattern Demonstration Summary

| Demo Step | Pattern Demonstrated | What you saw |
|---|---|---|
| Add Task | **Factory Method** | `TaskFactory.create()` made the right object type |
| View Schedule | **Singleton** | One planner, consistent state across all operations |
| Change Strategy | **Strategy** | Sort order changed live without restarting |
| Update Status | **Observer** | Three observers notified instantly |
| Import Calendar | **Adapter** | Incompatible `CalendarSystem` data converted seamlessly |
| Event Log | **Observer** | `LogNotifier` captured all events with timestamps |
