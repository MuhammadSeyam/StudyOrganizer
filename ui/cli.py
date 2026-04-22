"""
ui/cli.py
=========
Interactive Command-Line Interface (CLI) for the Smart Study Planner.

This module is purely presentation / input handling.
It contains zero business logic – everything is delegated to StudyPlanner.

Design responsibilities
-----------------------
- Parse user menu choices
- Gather and validate input
- Call planner methods and display results
- Demonstrate live switching of strategies (Strategy pattern)
- Demonstrate observer notifications (printed inside planner methods)
"""

from datetime import datetime
from typing import Optional

from models.task import TaskType, TaskStatus
from scheduler.planner import StudyPlanner
from patterns.strategy import SortByPriority, SortByDeadline, SortByDuration
from patterns.observer import ConsoleNotifier, DeadlineWatcher, LogNotifier
from patterns.adapter import CalendarSystem, TaskImportAdapter


# ── Colour helpers ─────────────────────────────────────────────────────────────

def _c(text: str, code: str) -> str:
    """Wrap text in an ANSI colour code."""
    return f"\033[{code}m{text}\033[0m"

CYAN    = "96"
YELLOW  = "93"
GREEN   = "92"
RED     = "91"
MAGENTA = "95"
BOLD    = "1"


# ── Input helpers ──────────────────────────────────────────────────────────────

def _input_int(prompt: str, min_val: int = None, max_val: int = None) -> Optional[int]:
    """Prompt for an integer; return None on invalid / empty input."""
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"  Value must be ≥ {min_val}. Using {min_val}.")
            return min_val
        if max_val is not None and val > max_val:
            print(f"  Value must be ≤ {max_val}. Using {max_val}.")
            return max_val
        return val
    except ValueError:
        print("  Invalid number. Skipping field.")
        return None


def _input_float(prompt: str) -> Optional[float]:
    """Prompt for a float; return None on invalid / empty input."""
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        print("  Invalid number. Skipping field.")
        return None


def _input_datetime(prompt: str) -> Optional[datetime]:
    """Prompt for a date/time in YYYY-MM-DD HH:MM format."""
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d %H:%M")
    except ValueError:
        print("  Invalid format. Please use YYYY-MM-DD HH:MM (e.g. 2026-05-20 14:00)")
        return None


def _choose_task_type() -> Optional[TaskType]:
    """Display task-type sub-menu and return the chosen TaskType."""
    print(f"\n  Task Types:")
    print(f"    {_c('1', YELLOW)} Study Task  (subject)")
    print(f"    {_c('2', YELLOW)} Exam Task   (course)")
    print(f"    {_c('3', YELLOW)} Break Task  (activity)")
    choice = input("  Choose type [1-3]: ").strip()
    mapping = {"1": TaskType.STUDY, "2": TaskType.EXAM, "3": TaskType.BREAK}
    if choice not in mapping:
        print("  Invalid choice.")
        return None
    return mapping[choice]


def _choose_status() -> Optional[TaskStatus]:
    """Display status sub-menu and return the chosen TaskStatus."""
    print(f"\n  Statuses:")
    print(f"    {_c('1', YELLOW)} Pending")
    print(f"    {_c('2', YELLOW)} In Progress")
    print(f"    {_c('3', YELLOW)} Done")
    choice = input("  Choose status [1-3]: ").strip()
    mapping = {
        "1": TaskStatus.PENDING,
        "2": TaskStatus.IN_PROGRESS,
        "3": TaskStatus.DONE,
    }
    if choice not in mapping:
        print("  Invalid choice.")
        return None
    return mapping[choice]


# ── Main Menu Actions ──────────────────────────────────────────────────────────

def action_add_task(planner: StudyPlanner) -> None:
    """Collect task details and add via the Singleton planner."""
    print(_c("\n  ── Add New Task ─────────────────────────────", CYAN))

    task_type = _choose_task_type()
    if task_type is None:
        return

    title = input("  Title: ").strip()
    if not title:
        print("  Title cannot be empty.")
        return

    priority = _input_int("  Priority [1=High … 5=Low]: ", 1, 5)
    if priority is None:
        priority = 3

    deadline = _input_datetime("  Deadline [YYYY-MM-DD HH:MM]: ")
    if deadline is None:
        print("  Deadline is required.")
        return

    duration = _input_float("  Estimated Duration (hours): ")
    if duration is None:
        duration = 1.0

    extra_kwargs = {}
    if task_type == TaskType.STUDY:
        subject = input("  Subject (e.g. Math, Physics): ").strip() or "General"
        extra_kwargs["subject"] = subject
    elif task_type == TaskType.EXAM:
        course = input("  Course name: ").strip() or "Unknown Course"
        extra_kwargs["course"] = course
    elif task_type == TaskType.BREAK:
        activity = input("  Activity (e.g. Walk, Coffee): ").strip() or "Rest"
        extra_kwargs["activity"] = activity

    task = planner.add_task(task_type, title, priority, deadline, duration, **extra_kwargs)
    print(_c(f"\n  ✅ Task #{task.task_id} '{task.title}' added successfully.", GREEN))


def action_edit_task(planner: StudyPlanner) -> None:
    """Edit an existing task's fields (leave blank to keep current value)."""
    print(_c("\n  ── Edit Task ────────────────────────────────", CYAN))

    task_id = _input_int("  Task ID to edit: ")
    if task_id is None:
        return

    task = planner.get_task(task_id)
    if task is None:
        print(_c(f"  Task #{task_id} not found.", RED))
        return

    print(f"  Current: {task}")
    print("  (Press ENTER to keep the current value)\n")

    title = input(f"  New Title [{task.title}]: ").strip() or None
    raw_priority = input(f"  New Priority [{task.priority}]: ").strip()
    priority = int(raw_priority) if raw_priority else None
    deadline = _input_datetime(f"  New Deadline [{task.deadline_str()}]: ")
    raw_duration = input(f"  New Duration [{task.duration}h]: ").strip()
    duration = float(raw_duration) if raw_duration else None

    planner.edit_task(task_id, title=title, priority=priority,
                      deadline=deadline, duration=duration)
    print(_c(f"\n  ✅ Task #{task_id} updated.", GREEN))


def action_delete_task(planner: StudyPlanner) -> None:
    """Delete a task by its ID."""
    print(_c("\n  ── Delete Task ──────────────────────────────", CYAN))
    task_id = _input_int("  Task ID to delete: ")
    if task_id is None:
        return
    task = planner.get_task(task_id)
    if task is None:
        print(_c(f"  Task #{task_id} not found.", RED))
        return
    confirm = input(f"  Delete '{task.title}'? [y/N]: ").strip().lower()
    if confirm == "y":
        planner.delete_task(task_id)
        print(_c(f"  🗑️  Task #{task_id} deleted.", RED))
    else:
        print("  Deletion cancelled.")


def action_update_status(planner: StudyPlanner) -> None:
    """Change the status of a task."""
    print(_c("\n  ── Update Task Status ───────────────────────", CYAN))
    task_id = _input_int("  Task ID: ")
    if task_id is None:
        return
    new_status = _choose_status()
    if new_status is None:
        return
    planner.update_status(task_id, new_status)
    print(_c(f"\n  ✅ Status updated.", GREEN))


def action_change_strategy(planner: StudyPlanner) -> None:
    """Switch sorting strategy at runtime (Strategy pattern demo)."""
    print(_c("\n  ── Change Scheduling Strategy ───────────────", CYAN))
    print(f"  Current strategy: {_c(planner.get_strategy_name(), YELLOW)}\n")
    print(f"  {_c('1', YELLOW)} Sort by Priority  (1 = highest first)")
    print(f"  {_c('2', YELLOW)} Sort by Deadline  (earliest first)")
    print(f"  {_c('3', YELLOW)} Sort by Duration  (shortest first)")

    choice = input("\n  Choose strategy [1-3]: ").strip()
    strategies = {
        "1": SortByPriority(),
        "2": SortByDeadline(),
        "3": SortByDuration(),
    }
    strategy = strategies.get(choice)
    if strategy is None:
        print("  Invalid choice.")
        return
    planner.set_strategy(strategy)
    print(_c(f"\n  ✅ Strategy switched to: {strategy.name}", GREEN))


def action_import_from_calendar(planner: StudyPlanner) -> None:
    """Demonstrate the Adapter pattern by importing from a mock calendar."""
    print(_c("\n  ── Import from External Calendar (Adapter) ──", CYAN))
    print("  Connecting to CalendarSystem (simulated external source)…\n")

    calendar = CalendarSystem()
    adapter  = TaskImportAdapter(calendar)
    tasks    = adapter.get_tasks()

    for task in tasks:
        planner.add_existing_task(task)

    print(_c(f"\n  ✅ {len(tasks)} tasks imported from CalendarSystem.", GREEN))


def action_show_overdue(planner: StudyPlanner) -> None:
    """List all overdue tasks."""
    print(_c("\n  ── Overdue Tasks ────────────────────────────", CYAN))
    overdue = planner.overdue_tasks()
    if not overdue:
        print("  🎉 No overdue tasks!")
    else:
        for task in overdue:
            print(f"  🚨 {task}")


def action_show_log(log_notifier: LogNotifier) -> None:
    """Print the full event log captured by LogNotifier."""
    print(_c("\n  ── Event Log (LogNotifier) ──────────────────", CYAN))
    log_notifier.show_logs()


# ── Main Menu ──────────────────────────────────────────────────────────────────

def print_menu() -> None:
    """Render the main menu."""
    print(_c("\n╔════════════════════════════════════════╗", CYAN))
    print(_c("║     🎓  Smart Study Planner  🎓         ║", CYAN))
    print(_c("╠════════════════════════════════════════╣", CYAN))
    print(f"  {_c('[1]', YELLOW)} View Schedule")
    print(f"  {_c('[2]', YELLOW)} Add Task")
    print(f"  {_c('[3]', YELLOW)} Edit Task")
    print(f"  {_c('[4]', YELLOW)} Delete Task")
    print(f"  {_c('[5]', YELLOW)} Update Task Status")
    print(f"  {_c('[6]', YELLOW)} Change Scheduling Strategy")
    print(f"  {_c('[7]', YELLOW)} Import from Calendar  (Adapter demo)")
    print(f"  {_c('[8]', YELLOW)} Show Overdue Tasks")
    print(f"  {_c('[9]', YELLOW)} Show Event Log")
    print(f"  {_c('[0]', RED  )} Exit")
    print(_c("╚════════════════════════════════════════╝", CYAN))


def run_cli() -> None:
    """
    Entry point for the interactive CLI.
    Sets up the singleton planner, wires up observers, and runs the menu loop.
    """
    # ── Singleton: one planner for the entire session ──────────────────────
    planner = StudyPlanner.get_instance()

    # ── Observer: register all listeners ──────────────────────────────────
    console_notifier  = ConsoleNotifier()
    deadline_watcher  = DeadlineWatcher(warning_hours=48)
    log_notifier      = LogNotifier()

    planner.register_observer(console_notifier)
    planner.register_observer(deadline_watcher)
    planner.register_observer(log_notifier)

    print(_c("\n  🎓 Welcome to Smart Study Planner!", BOLD))
    print("  Observers registered: ConsoleNotifier, DeadlineWatcher, LogNotifier")
    print("  Default strategy: Sort by Priority\n")

    # ── Main loop ──────────────────────────────────────────────────────────
    while True:
        print_menu()
        choice = input("  Choose option: ").strip()

        if   choice == "1": planner.display_schedule()
        elif choice == "2": action_add_task(planner)
        elif choice == "3": action_edit_task(planner)
        elif choice == "4": action_delete_task(planner)
        elif choice == "5": action_update_status(planner)
        elif choice == "6": action_change_strategy(planner)
        elif choice == "7": action_import_from_calendar(planner)
        elif choice == "8": action_show_overdue(planner)
        elif choice == "9": action_show_log(log_notifier)
        elif choice == "0":
            print(_c("\n  👋 Goodbye! Stay on schedule!\n", GREEN))
            break
        else:
            print(_c("  ❌ Invalid choice. Please try again.", RED))
