"""
patterns/adapter.py
===================
Implements the ADAPTER design pattern.

Pattern Intent
--------------
Convert the interface of a class into another interface that clients
expect.  Adapter lets classes work together that could not otherwise
because of incompatible interfaces.

How it is used here
-------------------
Scenario: An "external" calendar system (CalendarSystem) stores tasks
in a completely different format – a plain dictionary with different
key names and date formats.  The StudyPlanner cannot use CalendarSystem
directly because the interface is incompatible.

Solution:
- CalendarSystem     – the Adaptee (existing / external class, incompatible)
- TaskImportAdapter  – the Adapter (translates CalendarSystem → Task objects)
- StudyPlanner       – the Client (only calls adapter.get_tasks())

The adapter wraps CalendarSystem and exposes get_tasks() which returns
a proper List[Task] ready for the planner to consume – no changes needed
to CalendarSystem or StudyPlanner.

This simulates a real-world scenario: integrating with Google Calendar,
a university timetable API, or any legacy system.
"""

from datetime import datetime
from typing import List, Dict, Any

from models.task import Task, TaskType
from patterns.factory import TaskFactory


# ── Adaptee (simulated external / legacy system) ──────────────────────────────

class CalendarSystem:
    """
    Simulates an external calendar system with an incompatible interface.

    In a real project this could be:
    - A Google Calendar API client
    - A university timetable database reader
    - A JSON import from another app

    The format is a list of plain dictionaries with keys that do NOT
    match the Task constructor parameters.
    """

    def fetch_events(self) -> List[Dict[str, Any]]:
        """
        Returns raw calendar events – incompatible format.
        Key differences:
          "name"         → should be "title"
          "due"          → should be "deadline" (also a string, not datetime)
          "hours"        → should be "duration"
          "importance"   → should be "priority"
          "type"         → maps to TaskType (string, not enum)
          "extra_detail" → type-specific extra field
        """
        return [
            {
                "name":         "Physics Exam Prep",
                "due":          "2026-05-15 09:00",
                "hours":        3.0,
                "importance":   1,
                "type":         "Exam",
                "extra_detail": "Physics 301",
            },
            {
                "name":         "Read Chapter 7 – Networks",
                "due":          "2026-05-12 22:00",
                "hours":        1.5,
                "importance":   2,
                "type":         "Study",
                "extra_detail": "Computer Networks",
            },
            {
                "name":         "Afternoon Break",
                "due":          "2026-05-11 14:00",
                "hours":        0.5,
                "importance":   5,
                "type":         "Break",
                "extra_detail": "Coffee & walk",
            },
        ]


# ── Adapter ───────────────────────────────────────────────────────────────────

class TaskImportAdapter:
    """
    Adapts CalendarSystem's incompatible interface into Task objects.

    The planner calls:   adapter.get_tasks()  → List[Task]
    Internally it calls: calendar.fetch_events() and translates.
    """

    # Maps the external string "type" to the internal TaskType enum
    _TYPE_MAP: Dict[str, TaskType] = {
        "Study": TaskType.STUDY,
        "Exam":  TaskType.EXAM,
        "Break": TaskType.BREAK,
    }

    # Maps TaskType to the extra kwargs key
    _EXTRA_KEY: Dict[TaskType, str] = {
        TaskType.STUDY: "subject",
        TaskType.EXAM:  "course",
        TaskType.BREAK: "activity",
    }

    def __init__(self, calendar: CalendarSystem) -> None:
        self._calendar = calendar  # holds a reference to the Adaptee

    def get_tasks(self) -> List[Task]:
        """
        Translate CalendarSystem events into a List[Task] using the Factory.

        This is the only method the planner calls – it doesn't know anything
        about CalendarSystem's internal format.
        """
        raw_events = self._calendar.fetch_events()
        tasks: List[Task] = []

        for event in raw_events:
            task_type = self._TYPE_MAP.get(event["type"], TaskType.STUDY)
            extra_key = self._EXTRA_KEY[task_type]

            task = TaskFactory.create(
                task_type  = task_type,
                title      = event["name"],              # key translation
                priority   = event["importance"],        # key translation
                deadline   = datetime.strptime(          # type conversion
                                 event["due"],
                                 "%Y-%m-%d %H:%M"
                             ),
                duration   = event["hours"],             # key translation
                **{extra_key: event["extra_detail"]},   # dynamic extra kwarg
            )
            tasks.append(task)

        return tasks
