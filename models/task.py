"""
models/task.py
==============
Defines the base Task class and concrete task types.

Design Pattern Used: FACTORY METHOD (products)
- Task is the abstract product.
- StudyTask, ExamTask, and BreakTask are concrete products.
- The actual factory (TaskFactory) lives in patterns/factory.py.

Also demonstrates: SOLID - Open/Closed Principle
- You can add new task types without modifying existing code.
"""

from datetime import datetime
from enum import Enum


# ── Enumerations ────────────────────────────────────────────────────────────

class TaskType(Enum):
    """Supported task categories created by the Factory."""
    STUDY = "Study"
    EXAM  = "Exam"
    BREAK = "Break"


class TaskStatus(Enum):
    """Lifecycle states a task can be in."""
    PENDING     = "Pending"
    IN_PROGRESS = "In Progress"
    DONE        = "Done"


# ── Abstract / Base Task ─────────────────────────────────────────────────────

class Task:
    """
    Abstract base class for all task types.

    Attributes
    ----------
    task_id  : int       – Unique identifier (auto-assigned by factory)
    title    : str       – Short description of the task
    priority : int       – 1 (highest) … 5 (lowest)
    deadline : datetime  – When the task must be completed
    duration : float     – Estimated duration in hours
    status   : TaskStatus
    task_type: TaskType  – Set by each concrete subclass
    """

    _id_counter: int = 0  # class-level counter for unique IDs

    def __init__(
        self,
        title: str,
        priority: int,
        deadline: datetime,
        duration: float,
    ) -> None:
        Task._id_counter += 1
        self.task_id:   int        = Task._id_counter
        self.title:     str        = title
        self.priority:  int        = max(1, min(5, priority))   # clamp 1-5
        self.deadline:  datetime   = deadline
        self.duration:  float      = duration
        self.status:    TaskStatus = TaskStatus.PENDING
        self.task_type: TaskType   = None   # set by subclass

    # ── Helpers ──────────────────────────────────────────────────────────────

    def mark_in_progress(self) -> None:
        """Transition task to IN_PROGRESS."""
        self.status = TaskStatus.IN_PROGRESS

    def mark_done(self) -> None:
        """Transition task to DONE."""
        self.status = TaskStatus.DONE

    def mark_pending(self) -> None:
        """Reset task back to PENDING."""
        self.status = TaskStatus.PENDING

    def is_overdue(self) -> bool:
        """Return True if deadline has passed and task is not done."""
        return self.status != TaskStatus.DONE and datetime.now() > self.deadline

    def deadline_str(self) -> str:
        """Human-readable deadline."""
        return self.deadline.strftime("%Y-%m-%d %H:%M")

    def __repr__(self) -> str:
        return (
            f"[{self.task_type.value if self.task_type else 'Task'} #{self.task_id}] "
            f"'{self.title}' | Priority:{self.priority} | "
            f"Deadline:{self.deadline_str()} | Duration:{self.duration}h | "
            f"Status:{self.status.value}"
        )


# ── Concrete Task Types (Factory Method – Products) ──────────────────────────

class StudyTask(Task):
    """
    A regular study / revision task.
    Extra attribute: subject – the subject being studied.
    """

    def __init__(
        self,
        title:    str,
        priority: int,
        deadline: datetime,
        duration: float,
        subject:  str = "General",
    ) -> None:
        super().__init__(title, priority, deadline, duration)
        self.task_type: TaskType = TaskType.STUDY
        self.subject:   str      = subject

    def __repr__(self) -> str:
        return super().__repr__() + f" | Subject:{self.subject}"


class ExamTask(Task):
    """
    An exam preparation task.
    Extra attribute: course – the course the exam belongs to.
    """

    def __init__(
        self,
        title:    str,
        priority: int,
        deadline: datetime,
        duration: float,
        course:   str = "Unknown Course",
    ) -> None:
        super().__init__(title, priority, deadline, duration)
        self.task_type: TaskType = TaskType.EXAM
        self.course:    str      = course

    def __repr__(self) -> str:
        return super().__repr__() + f" | Course:{self.course}"


class BreakTask(Task):
    """
    A scheduled rest/break between heavy study sessions.
    Extra attribute: activity – what to do during the break.
    """

    def __init__(
        self,
        title:    str,
        priority: int,
        deadline: datetime,
        duration: float,
        activity: str = "Rest",
    ) -> None:
        super().__init__(title, priority, deadline, duration)
        self.task_type: TaskType = TaskType.BREAK
        self.activity:  str      = activity

    def __repr__(self) -> str:
        return super().__repr__() + f" | Activity:{self.activity}"
