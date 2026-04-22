"""
patterns/strategy.py
====================
Implements the STRATEGY design pattern.

Pattern Intent
--------------
Define a family of algorithms, encapsulate each one, and make them
interchangeable. Strategy lets the algorithm vary independently from
clients that use it.

How it is used here
-------------------
- SortStrategy is the abstract strategy (interface).
- SortByPriority, SortByDeadline, and SortByDuration are the three
  concrete strategies.
- The StudyPlanner (context) holds a reference to the current strategy
  and calls strategy.sort(tasks) whenever it needs to display or process
  the schedule.
- Switching strategies at runtime (without rewriting planner logic)
  perfectly demonstrates the pattern's power.

Relation to SOLID
-----------------
- Open/Closed Principle: Adding a new strategy (e.g., SortBySubject)
  requires zero changes to the planner or existing strategies.
- Single Responsibility: Each strategy class has exactly one job –
  sorting tasks by a specific criterion.
"""

from abc import ABC, abstractmethod
from typing import List
from models.task import Task


# ── Abstract Strategy ─────────────────────────────────────────────────────────

class SortStrategy(ABC):
    """
    Abstract base class all sort strategies must implement.
    """

    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        """
        Return a NEW sorted list of tasks (do NOT modify the original list).

        Parameters
        ----------
        tasks : List[Task] – the current task list from the planner

        Returns
        -------
        List[Task] – sorted copy
        """
        pass

    @property
    def name(self) -> str:
        """Human-readable strategy name (used in UI output)."""
        return self.__class__.__name__


# ── Concrete Strategies ───────────────────────────────────────────────────────

class SortByPriority(SortStrategy):
    """
    Strategy 1 – Sort tasks by priority (1 = highest first).

    Use-case: When the student wants to tackle the most important tasks
    first, regardless of when they are due.
    """

    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.priority)

    @property
    def name(self) -> str:
        return "Sort by Priority (1=Highest)"


class SortByDeadline(SortStrategy):
    """
    Strategy 2 – Sort tasks by deadline (earliest first).

    Use-case: When the student wants to see what is due soonest –
    ideal for cramming the night before exams.
    """

    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.deadline)

    @property
    def name(self) -> str:
        return "Sort by Deadline (Earliest First)"


class SortByDuration(SortStrategy):
    """
    Strategy 3 – Sort tasks by estimated duration (shortest first).

    Use-case: 'Eat the frog' reversed – clear quick wins first to
    build momentum, leaving longer tasks for dedicated study blocks.
    """

    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.duration)

    @property
    def name(self) -> str:
        return "Sort by Duration (Shortest First)"
