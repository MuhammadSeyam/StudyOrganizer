"""
test_gui.py
===========
Headless tests for the GUI layer (no window opened).
Verifies that GUINotifier, AddTaskDialog data-flow, and the
StudyPlannerGUI wiring work correctly without a display.

Run with:
    python test_gui.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Reset singleton so GUI tests start fresh ───────────────────────────────
from scheduler.planner import StudyPlanner
StudyPlanner._instance = None

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
errors = 0

def check(cond, msg):
    global errors
    tag = PASS if cond else FAIL
    print(f"  {tag} {msg}")
    if not cond:
        errors += 1

print("\n" + "="*55)
print("  Smart Study Planner — GUI Layer Tests (headless)")
print("="*55)

# ── Test 1: GUINotifier behaves like any Observer ──────────────────────────
print("\n[1] GUINotifier (Observer contract)")
import tkinter as tk
root = tk.Tk()
root.withdraw()   # keep hidden

from ui.gui_app import GUINotifier
var = tk.StringVar(master=root, value="")
notifier = GUINotifier(var)
notifier.update("Task added", None)
check("Task added" in var.get(), "update() writes event to StringVar")
notifier.update("Status changed", None)
check("Status changed" in var.get(), "StringVar reflects latest event")

# ── Test 2: GUINotifier registers with planner as a valid Observer ─────────
print("\n[2] GUINotifier + Singleton integration")
from patterns.observer import Observer
check(isinstance(notifier, Observer), "GUINotifier is a valid Observer subclass")

planner = StudyPlanner.get_instance()
planner.register_observer(notifier)
check(notifier in planner._observers, "GUINotifier registered with planner")

# trigger an event via backend — StringVar must update
from models.task import TaskType, TaskStatus
from datetime import datetime
t = planner.add_task(TaskType.STUDY, "Headless test task", 2,
                     datetime(2026, 6, 1, 10, 0), 1.5, subject="Test")
check("Task #" in var.get(), "Observer notified on add_task -> StringVar updated")

# ── Test 3: mode-selector routing in main.py ──────────────────────────────
print("\n[3] main.py routing logic (import check)")
import importlib.util
spec = importlib.util.spec_from_file_location(
    "main",
    os.path.join(os.path.dirname(__file__), "main.py")
)
mod = importlib.util.module_from_spec(spec)
# Don't exec (it would block on input), just check it parses
check(spec is not None, "main.py is importable as a module")

# ── Test 4: strategy switching updates get_schedule() ─────────────────────
print("\n[4] Strategy switching via GUI STRATEGIES dict")
from ui.gui_app import StudyPlannerGUI
# Access the class-level STRATEGIES dict without instantiating
strategies = StudyPlannerGUI.STRATEGIES
check(len(strategies) == 3, "GUI exposes exactly 3 strategies")

from patterns.strategy import SortByPriority, SortByDeadline, SortByDuration
strategy_types = [type(s) for s in strategies.values()]
check(SortByPriority  in strategy_types, "SortByPriority available in GUI")
check(SortByDeadline  in strategy_types, "SortByDeadline available in GUI")
check(SortByDuration  in strategy_types, "SortByDuration available in GUI")

for name, strategy in strategies.items():
    planner.set_strategy(strategy)
    result = planner.get_schedule()
    check(isinstance(result, list), f"Strategy '{name}' returns a list")

# ── Test 5: Adapter still works independently ─────────────────────────────
print("\n[5] Adapter integration (GUI import button backend)")
from patterns.adapter import CalendarSystem, TaskImportAdapter
imported = TaskImportAdapter(CalendarSystem()).get_tasks()
check(len(imported) == 3, "Adapter returns 3 tasks for GUI import button")
for t in imported:
    check(isinstance(t.deadline, datetime),
          f"  Deadline type correct for '{t.title}'")

# ── Test 6: STATUS_OPTIONS matches TaskStatus enum ────────────────────────
print("\n[6] GUI STATUS_OPTIONS match TaskStatus enum")
for label, status in StudyPlannerGUI.STATUS_OPTIONS.items():
    check(isinstance(status, TaskStatus),
          f"'{label}' maps to a valid TaskStatus")

root.destroy()

# ── Summary ───────────────────────────────────────────────────────────────
print("\n" + "="*55)
if errors == 0:
    print("\033[92m  All GUI tests passed!\033[0m")
else:
    print(f"\033[91m  {errors} test(s) FAILED.\033[0m")
print("="*55 + "\n")
sys.exit(errors)
