"""
scheduler/planner.py
====================
The central StudyPlanner – the heart of the system.

Design Patterns Used Here
--------------------------
1. SINGLETON
   StudyPlanner ensures only ONE instance ever exists.
   All code that calls StudyPlanner.get_instance() receives the same object.

2. OBSERVER (Subject role)
   StudyPlanner inherits from Subject (patterns/observer.py).
   It calls self.notify_observers() after every meaningful state change.

3. STRATEGY (Context role)
   StudyPlanner holds a SortStrategy reference.
   Calling set_strategy() swaps the algorithm at runtime.
   get_schedule() delegates sorting to the current strategy.

This single class wires Singleton + Observer + Strategy together, proving
that patterns are composable and complementary.
"""

from typing import List, Optional
from datetime import datetime

from models.task import Task, TaskType, TaskStatus
from patterns.observer import Subject
from patterns.strategy import SortStrategy, SortByPriority
from patterns.factory import TaskFactory


class StudyPlanner(Subject):
    """
    Singleton + Observer Subject + Strategy Context.

    Creation
    --------
    DO NOT call StudyPlanner() directly.
    Always use: planner = StudyPlanner.get_instance()

    Responsibilities
    ----------------
    - Maintain the master task list.
    - Delegate task creation to TaskFactory (Factory Method pattern).
    - Sort/display the schedule via the active SortStrategy.
    - Notify all registered observers whenever state changes.
    """

    # ── Singleton internals ───────────────────────────────────────────────────
    _instance: "StudyPlanner" = None  # the one and only instance

    def __new__(cls) -> "StudyPlanner":
        """
        Override __new__ to enforce the Singleton guarantee.
        If an instance already exists, return it; otherwise create one.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> "StudyPlanner":
        """Public accessor – always returns the singleton."""
        if cls._instance is None:
            cls()  # triggers __new__ → creates instance
        return cls._instance

    # ── Initialisation (runs once) ────────────────────────────────────────────

    def __init__(self) -> None:
        if self._initialized:
            return  # prevent re-initialisation on subsequent calls
        super().__init__()                    # initialise Subject (observers list)
        self._tasks: List[Task] = []
        self._strategy: SortStrategy = SortByPriority()  # default strategy
        self._initialized = True

    # ── Strategy setter ───────────────────────────────────────────────────────

    def set_strategy(self, strategy: SortStrategy) -> None:
        """
        Swap the active sort strategy at runtime (Strategy pattern).

        Parameters
        ----------
        strategy : SortStrategy – any concrete strategy implementation
        """
        self._strategy = strategy
        self.notify_observers(
            f"Scheduling strategy changed to: {strategy.name}"
        )

    def get_strategy_name(self) -> str:
        return self._strategy.name

    # ── Task CRUD ─────────────────────────────────────────────────────────────

    def add_task(
        self,
        task_type: TaskType,
        title:     str,
        priority:  int,
        deadline:  datetime,
        duration:  float,
        **extra_kwargs,
    ) -> Task:
        """
        Create and register a new task via the Factory, then notify observers.

        Returns
        -------
        Task – the newly created task object.
        """
        task = TaskFactory.create(
            task_type  = task_type,
            title      = title,
            priority   = priority,
            deadline   = deadline,
            duration   = duration,
            **extra_kwargs,
        )
        self._tasks.append(task)
        self.notify_observers("Task added", task)
        return task

    def add_existing_task(self, task: Task) -> None:
        """
        Register an already-constructed Task object (e.g., from the Adapter).
        """
        self._tasks.append(task)
        self.notify_observers("Task imported from external source", task)

    def edit_task(
        self,
        task_id:   int,
        title:     Optional[str]     = None,
        priority:  Optional[int]     = None,
        deadline:  Optional[datetime] = None,
        duration:  Optional[float]   = None,
    ) -> Optional[Task]:
        """
        Update one or more fields of an existing task.

        Parameters
        ----------
        task_id  : int – the unique task ID to find and edit
        (remaining parameters are optional; only supplied ones are updated)

        Returns
        -------
        Task if found and updated, None otherwise.
        """
        task = self._find_task(task_id)
        if task is None:
            print(f"  [ERROR] Task #{task_id} not found.")
            return None

        if title    is not None: task.title    = title
        if priority is not None: task.priority = max(1, min(5, priority))
        if deadline is not None: task.deadline = deadline
        if duration is not None: task.duration = duration

        self.notify_observers("Task updated", task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the planner by its ID.

        Returns True if removed, False if not found.
        """
        task = self._find_task(task_id)
        if task is None:
            print(f"  [ERROR] Task #{task_id} not found.")
            return False
        self._tasks.remove(task)
        self.notify_observers(f"Task deleted: '{task.title}'", task)
        return True

    def update_status(self, task_id: int, new_status: TaskStatus) -> Optional[Task]:
        """
        Change the status of a task (Pending / In Progress / Done).

        Triggers an observer notification so the UI / log stays in sync.
        """
        task = self._find_task(task_id)
        if task is None:
            print(f"  [ERROR] Task #{task_id} not found.")
            return None
        task.status = new_status
        self.notify_observers(
            f"Status changed to '{new_status.value}'", task
        )
        return task

    # ── Schedule display ──────────────────────────────────────────────────────

    def get_schedule(self) -> List[Task]:
        """
        Return tasks sorted by the current strategy.
        Does NOT modify the internal _tasks list.
        """
        return self._strategy.sort(self._tasks)

    def display_schedule(self) -> None:
        """
        Pretty-print the current schedule to stdout.
        """
        sorted_tasks = self.get_schedule()
        strategy_name = self._strategy.name

        border = "═" * 72
        print(f"\n  ╔{border}╗")
        print(f"  ║  📅  SMART STUDY PLANNER  –  {strategy_name:<38}║")
        print(f"  ╠{border}╣")

        if not sorted_tasks:
            print(f"  ║  (No tasks yet. Add some tasks to get started!){'':>22}║")
        else:
            for idx, task in enumerate(sorted_tasks, start=1):
                type_icon = {"Study": "📖", "Exam": "📝", "Break": "☕"}.get(
                    task.task_type.value, "📌"
                )
                status_icon = {
                    "Pending":     "⏳",
                    "In Progress": "🔄",
                    "Done":        "✅",
                }.get(task.status.value, "❓")
                overdue_flag = " 🚨OVERDUE" if task.is_overdue() else ""

                print(f"  ║  {idx:>2}. {type_icon} [{task.task_type.value:<5}] "
                      f"#{task.task_id:<3} {task.title:<25} {status_icon} {task.status.value:<11}"
                      f"║")
                print(f"  ║      Priority:{task.priority}  "
                      f"Deadline:{task.deadline_str()}  "
                      f"Duration:{task.duration}h{overdue_flag:<12}  ║")
                if idx < len(sorted_tasks):
                    print(f"  ╠{'─' * 72}╣")

        print(f"  ╚{border}╝")
        print(f"  Total tasks: {len(self._tasks)}\n")

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._find_task(task_id)

    def all_tasks(self) -> List[Task]:
        return list(self._tasks)

    def pending_tasks(self) -> List[Task]:
        return [t for t in self._tasks if t.status == TaskStatus.PENDING]

    def overdue_tasks(self) -> List[Task]:
        return [t for t in self._tasks if t.is_overdue()]

    # ── Private helper ────────────────────────────────────────────────────────

    def _find_task(self, task_id: int) -> Optional[Task]:
        """Linear search for a task by its unique ID."""
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        return None
