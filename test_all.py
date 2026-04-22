"""
test_all.py
===========
Automated verification script — run once to confirm all patterns work.
Usage:
    cd SmartStudyPlanner
    python test_all.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from models.task import TaskType, TaskStatus
from scheduler.planner import StudyPlanner
from patterns.strategy import SortByPriority, SortByDeadline, SortByDuration
from patterns.observer import LogNotifier, ConsoleNotifier
from patterns.adapter import CalendarSystem, TaskImportAdapter

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
errors = 0

def check(condition, msg):
    global errors
    if condition:
        print(f"  {PASS} {msg}")
    else:
        print(f"  {FAIL} {msg}")
        errors += 1

print("\n" + "="*55)
print("  Smart Study Planner — Automated Test Suite")
print("="*55)

# ── Reset singleton state between test runs ────────────────
StudyPlanner._instance = None

# ─────────────────────────────────────────────────────────────
# Test 1: Singleton
# ─────────────────────────────────────────────────────────────
print("\n[1] SINGLETON PATTERN")
p1 = StudyPlanner.get_instance()
p2 = StudyPlanner.get_instance()
check(p1 is p2, "get_instance() always returns the same object")
check(type(p1).__name__ == "StudyPlanner", "Instance is a StudyPlanner")

# ─────────────────────────────────────────────────────────────
# Test 2: Factory Method
# ─────────────────────────────────────────────────────────────
print("\n[2] FACTORY METHOD PATTERN")
dl_exam  = datetime(2026, 5, 30,  9, 0)
dl_study = datetime(2026, 6,  1, 10, 0)
dl_break = datetime(2026, 5, 28, 12, 0)

planner = StudyPlanner.get_instance()

t_exam  = planner.add_task(TaskType.EXAM,  "Final Exam Prep",   1, dl_exam,  3.0, course="CS201")
t_study = planner.add_task(TaskType.STUDY, "Revise Chapter 5",  2, dl_study, 1.5, subject="Math")
t_break = planner.add_task(TaskType.BREAK, "Coffee Break",      5, dl_break, 0.5, activity="Walk")

check(t_exam.task_type  == TaskType.EXAM,  "Factory creates ExamTask correctly")
check(t_study.task_type == TaskType.STUDY, "Factory creates StudyTask correctly")
check(t_break.task_type == TaskType.BREAK, "Factory creates BreakTask correctly")
check(t_exam.course  == "CS201", "ExamTask has 'course' attribute")
check(t_study.subject == "Math", "StudyTask has 'subject' attribute")
check(t_break.activity == "Walk", "BreakTask has 'activity' attribute")
check(len(planner.all_tasks()) == 3, "Planner holds exactly 3 tasks")

# ─────────────────────────────────────────────────────────────
# Test 3: Strategy Pattern
# ─────────────────────────────────────────────────────────────
print("\n[3] STRATEGY PATTERN")

planner.set_strategy(SortByDeadline())
sched = planner.get_schedule()
check(sched[0].task_id == t_break.task_id,
      f"SortByDeadline: first = #{t_break.task_id} '{t_break.title}'")

planner.set_strategy(SortByDuration())
sched = planner.get_schedule()
check(sched[0].task_id == t_break.task_id,
      f"SortByDuration: first = #{t_break.task_id} '{t_break.title}' (0.5h)")

planner.set_strategy(SortByPriority())
sched = planner.get_schedule()
check(sched[0].task_id == t_exam.task_id,
      f"SortByPriority: first = #{t_exam.task_id} '{t_exam.title}' (priority 1)")

check(planner.get_strategy_name() == "Sort by Priority (1=Highest)",
      "Strategy name reported correctly")

# ─────────────────────────────────────────────────────────────
# Test 4: Observer Pattern
# ─────────────────────────────────────────────────────────────
print("\n[4] OBSERVER PATTERN")
log = LogNotifier()
planner.register_observer(log)

initial_log_count = len(log.logs)

planner.update_status(t_study.task_id, TaskStatus.IN_PROGRESS)
check(t_study.status == TaskStatus.IN_PROGRESS,
      "update_status() changes task status correctly")
check(len(log.logs) > initial_log_count,
      "LogNotifier captured the status-change event")

planner.edit_task(t_exam.task_id, title="Final Exam Prep (Updated)")
check(planner.get_task(t_exam.task_id).title == "Final Exam Prep (Updated)",
      "edit_task() updates title")
check(len(log.logs) >= 2,
      "LogNotifier captured the edit event")

# Remove observer and check it no longer receives events
planner.remove_observer(log)
count_before = len(log.logs)
planner.update_status(t_break.task_id, TaskStatus.DONE)
check(len(log.logs) == count_before,
      "remove_observer() stops notifications correctly")

# ─────────────────────────────────────────────────────────────
# Test 5: Adapter Pattern
# ─────────────────────────────────────────────────────────────
print("\n[5] ADAPTER PATTERN")
calendar = CalendarSystem()
adapter  = TaskImportAdapter(calendar)
imported = adapter.get_tasks()

check(len(imported) == 3, "Adapter imports exactly 3 tasks from CalendarSystem")
check(imported[0].task_type == TaskType.EXAM,  "First imported task is ExamTask")
check(imported[1].task_type == TaskType.STUDY, "Second imported task is StudyTask")
check(imported[2].task_type == TaskType.BREAK, "Third imported task is BreakTask")

for t in imported:
    check(isinstance(t.deadline, datetime),
          f"Adapter converted deadline correctly for '{t.title}'")

# Add imported tasks to planner
for t in imported:
    planner.add_existing_task(t)
check(len(planner.all_tasks()) == 6,
      "Planner now holds 6 tasks (3 original + 3 imported)")

# ─────────────────────────────────────────────────────────────
# Test 6: Delete
# ─────────────────────────────────────────────────────────────
print("\n[6] DELETE")
removed = planner.delete_task(t_break.task_id)
check(removed, "delete_task() returns True on success")
check(planner.get_task(t_break.task_id) is None,
      "Deleted task is gone from planner")
check(len(planner.all_tasks()) == 5, "Planner has 5 tasks after deletion")

# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────
print("\n" + "="*55)
if errors == 0:
    print("\033[92m  All tests passed! Project is fully functional.\033[0m")
else:
    print(f"\033[91m  {errors} test(s) FAILED — review output above.\033[0m")
print("="*55 + "\n")
sys.exit(errors)
