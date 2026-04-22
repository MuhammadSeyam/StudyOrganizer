"""
patterns/factory.py
===================
Implements the FACTORY METHOD design pattern.

Pattern Intent
--------------
Define an interface for creating an object, but let subclasses decide
which class to instantiate.  Factory Method lets a class defer
instantiation to subclasses.

How it is used here
-------------------
- TaskFactory is the Creator class with a single static factory method:
      TaskFactory.create(task_type, **kwargs) → Task

- Instead of calling StudyTask(...), ExamTask(...) or BreakTask(...)
  directly from the planner or UI, all task creation is centralised here.
  The caller only needs to know the desired TaskType enum value and the
  common task arguments.

- This decouples object creation from the rest of the system:
  if a new task type (e.g., ProjectTask) is added, only this file
  needs to change – the planner, UI, and tests stay untouched.

Relation to SOLID
-----------------
- Single Responsibility: The factory's only job is to construct Task objects.
- Open/Closed: New task types → extend the registry, not modify callers.
- Dependency Inversion: Higher-level modules depend on the abstract Task,
  not on concrete StudyTask/ExamTask/BreakTask.
"""

from datetime import datetime
from models.task import Task, TaskType, StudyTask, ExamTask, BreakTask


class TaskFactory:
    """
    Central factory for creating Task objects.

    Usage
    -----
    task = TaskFactory.create(
        task_type = TaskType.STUDY,
        title     = "Revise Chapter 5",
        priority  = 2,
        deadline  = datetime(2026, 5, 10, 18, 0),
        duration  = 1.5,
        subject   = "Software Engineering",
    )
    """

    # Maps each TaskType to its concrete class.
    # To support a new type: just add one entry here.
    _registry: dict = {
        TaskType.STUDY: StudyTask,
        TaskType.EXAM:  ExamTask,
        TaskType.BREAK: BreakTask,
    }

    @staticmethod
    def create(
        task_type: TaskType,
        title:     str,
        priority:  int,
        deadline:  datetime,
        duration:  float,
        **extra_kwargs,
    ) -> Task:
        """
        Instantiate and return the appropriate Task subclass.

        Parameters
        ----------
        task_type    : TaskType   – which type to create
        title        : str        – task title
        priority     : int        – 1 (high) … 5 (low)
        deadline     : datetime   – due date/time
        duration     : float      – estimated hours
        **extra_kwargs            – type-specific arguments:
            StudyTask → subject="Math"
            ExamTask  → course="Data Structures"
            BreakTask → activity="Walk"

        Returns
        -------
        Task – concrete subclass instance

        Raises
        ------
        ValueError if task_type is not registered.
        """
        task_class = TaskFactory._registry.get(task_type)
        if task_class is None:
            supported = [t.value for t in TaskFactory._registry]
            raise ValueError(
                f"Unknown task type '{task_type}'. "
                f"Supported types: {supported}"
            )

        return task_class(
            title    = title,
            priority = priority,
            deadline = deadline,
            duration = duration,
            **extra_kwargs,
        )

    @staticmethod
    def supported_types() -> list:
        """Return a list of all registered TaskType values."""
        return list(TaskFactory._registry.keys())
