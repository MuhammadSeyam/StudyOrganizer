"""
patterns/observer.py
====================
Implements the OBSERVER design pattern.

Pattern Intent
--------------
Define a one-to-many dependency between objects so that when one object
(the Subject / Publisher) changes state, all its dependents (Observers)
are notified and updated automatically.

How it is used here
-------------------
- The StudyPlanner (in scheduler/planner.py) acts as the SUBJECT.
- Whenever a task is added, edited, deleted, or its status changes, the
  planner calls notify_observers() which loops through all registered
  observers and calls their update() method.

Concrete Observers
------------------
1. ConsoleNotifier  – prints a coloured message to stdout.
2. DeadlineWatcher  – specifically warns when a task deadline is very close.
3. LogNotifier      – appends events to an in-memory log list (simulates
                      writing to a file; useful for testing).
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List


# ── Abstract Observer ─────────────────────────────────────────────────────────

class Observer(ABC):
    """
    Abstract base class every observer must implement.
    """

    @abstractmethod
    def update(self, event: str, task=None) -> None:
        """
        Called by the subject when something noteworthy happens.

        Parameters
        ----------
        event : str  – human-readable description of what happened
        task  : Task – the task involved (may be None for global events)
        """
        pass


# ── Abstract Subject (interface the planner will implement) ───────────────────

class Subject(ABC):
    """
    Abstract Subject that can register / remove / notify observers.
    The StudyPlanner inherits from this.
    """

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def register_observer(self, observer: Observer) -> None:
        """Attach a new observer."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """Detach an observer."""
        self._observers.remove(observer)

    def notify_observers(self, event: str, task=None) -> None:
        """Push event to every registered observer."""
        for obs in self._observers:
            obs.update(event, task)


# ── Concrete Observers ────────────────────────────────────────────────────────

class ConsoleNotifier(Observer):
    """
    Prints a formatted notification to the console whenever an event fires.
    This is the simplest observer – great for demo and real-time feedback.
    """

    # ANSI colour codes for a nicer terminal experience
    COLOURS = {
        "added":   "\033[92m",   # green
        "deleted": "\033[91m",   # red
        "edited":  "\033[93m",   # yellow
        "status":  "\033[96m",   # cyan
        "warning": "\033[95m",   # magenta
        "reset":   "\033[0m",
    }

    def update(self, event: str, task=None) -> None:
        colour_key = "warning" if "warning" in event.lower() or "urgent" in event.lower() else \
                     "added"   if "added"   in event.lower() else \
                     "deleted" if "deleted" in event.lower() else \
                     "edited"  if "edited"  in event.lower() or "updated" in event.lower() else \
                     "status"
        colour = self.COLOURS.get(colour_key, "")
        reset  = self.COLOURS["reset"]
        task_info = f" → Task #{task.task_id} '{task.title}'" if task else ""
        print(f"  🔔 {colour}[NOTIFICATION]{reset} {event}{task_info}")


class DeadlineWatcher(Observer):
    """
    Watches for tasks whose deadline is approaching within a warning window
    (default: 24 hours).  Fires an additional urgent notice when relevant.
    """

    def __init__(self, warning_hours: int = 24) -> None:
        self.warning_hours = warning_hours

    def update(self, event: str, task=None) -> None:
        if task is None:
            return
        time_left = task.deadline - datetime.now()
        if timedelta(0) < time_left <= timedelta(hours=self.warning_hours):
            hours_left = int(time_left.total_seconds() // 3600)
            print(
                f"  ⚠️  \033[95m[DEADLINE WARNING]\033[0m Task #{task.task_id} "
                f"'{task.title}' is due in ~{hours_left} hour(s)!"
            )
        elif time_left < timedelta(0) and task.status.value != "Done":
            print(
                f"  🚨 \033[91m[OVERDUE]\033[0m Task #{task.task_id} "
                f"'{task.title}' is OVERDUE!"
            )


class LogNotifier(Observer):
    """
    Keeps an in-memory list of all events (simulates a log file).
    Useful for auditing, testing, and future persistence features.
    """

    def __init__(self) -> None:
        self.logs: List[str] = []

    def update(self, event: str, task=None) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_info = f" | Task #{task.task_id}" if task else ""
        entry = f"[{timestamp}]{task_info} – {event}"
        self.logs.append(entry)

    def show_logs(self) -> None:
        """Print all recorded log entries."""
        if not self.logs:
            print("  (No log entries yet.)")
            return
        print("\n  ── Event Log ──────────────────────────────")
        for entry in self.logs:
            print(f"  {entry}")
        print("  ───────────────────────────────────────────\n")
