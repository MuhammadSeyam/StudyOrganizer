"""
ui/gui_app.py
=============
Tkinter GUI — presentation layer ONLY.

ALL business logic stays in the backend:
  • StudyPlanner.get_instance()  → Singleton
  • TaskFactory                  → Factory Method
  • SortBy* strategies           → Strategy
  • ConsoleNotifier / LogNotifier → Observer (still active)
  • GUINotifier (below)          → new Observer that updates the GUI status bar

Architecture rule: this file may ONLY import from models/, patterns/, scheduler/.
It must NEVER re-implement any business logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── Backend imports (shared with CLI – nothing duplicated) ─────────────────
from models.task import TaskType, TaskStatus
from patterns.observer import Observer, ConsoleNotifier, LogNotifier
from patterns.strategy import SortByPriority, SortByDeadline, SortByDuration
from patterns.adapter import CalendarSystem, TaskImportAdapter
from scheduler.planner import StudyPlanner


# ═══════════════════════════════════════════════════════════════════════════
# GUINotifier  –  Observer that pushes events into the GUI status bar
# ═══════════════════════════════════════════════════════════════════════════

class GUINotifier(Observer):
    """
    Concrete Observer for the GUI.
    Receives the same event calls as ConsoleNotifier / LogNotifier,
    but instead of printing to stdout it updates a Tkinter StringVar
    so the status bar at the bottom of the window refreshes live.
    """
    def __init__(self, status_var: tk.StringVar) -> None:
        self._var = status_var

    def update(self, event: str, task=None) -> None:
        task_info = f"  ·  Task #{task.task_id} '{task.title}'" if task else ""
        self._var.set(f"🔔  {event}{task_info}")


# ═══════════════════════════════════════════════════════════════════════════
# AddTaskDialog  –  modal form for creating a new task
# ═══════════════════════════════════════════════════════════════════════════

class AddTaskDialog(tk.Toplevel):
    """Modal dialog that collects all fields needed to create a Task."""

    TYPES    = ["Study", "Exam", "Break"]
    EXTRA_LBL = {"Study": "Subject", "Exam": "Course", "Break": "Activity"}

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Task")
        self.resizable(False, False)
        self.grab_set()          # make it modal
        self.result = None       # filled on OK

        self._build()
        self.wait_window()

    # ── Layout ────────────────────────────────────────────────────────────
    def _build(self):
        pad = {"padx": 10, "pady": 5}
        f   = ttk.Frame(self, padding=10)
        f.pack(fill="both", expand=True)

        # Task type
        ttk.Label(f, text="Task Type:").grid(row=0, column=0, sticky="w", **pad)
        self._type_var = tk.StringVar(value="Study")
        cb = ttk.Combobox(f, textvariable=self._type_var,
                          values=self.TYPES, state="readonly", width=18)
        cb.grid(row=0, column=1, sticky="w", **pad)
        cb.bind("<<ComboboxSelected>>", self._on_type_change)

        # Title
        ttk.Label(f, text="Title:").grid(row=1, column=0, sticky="w", **pad)
        self._title = ttk.Entry(f, width=30)
        self._title.grid(row=1, column=1, sticky="w", **pad)

        # Priority
        ttk.Label(f, text="Priority (1-5):").grid(row=2, column=0, sticky="w", **pad)
        self._priority = ttk.Spinbox(f, from_=1, to=5, width=5)
        self._priority.set(3)
        self._priority.grid(row=2, column=1, sticky="w", **pad)

        # Deadline
        ttk.Label(f, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=3, column=0, sticky="w", **pad)
        self._deadline = ttk.Entry(f, width=20)
        self._deadline.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self._deadline.grid(row=3, column=1, sticky="w", **pad)

        # Duration
        ttk.Label(f, text="Duration (hours):").grid(row=4, column=0, sticky="w", **pad)
        self._duration = ttk.Entry(f, width=8)
        self._duration.insert(0, "1.0")
        self._duration.grid(row=4, column=1, sticky="w", **pad)

        # Dynamic extra field (subject / course / activity)
        self._extra_lbl_var = tk.StringVar(value="Subject:")
        ttk.Label(f, textvariable=self._extra_lbl_var).grid(row=5, column=0, sticky="w", **pad)
        self._extra = ttk.Entry(f, width=30)
        self._extra.grid(row=5, column=1, sticky="w", **pad)

        # Buttons
        btn_f = ttk.Frame(f)
        btn_f.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(btn_f, text="Add Task", command=self._ok).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Cancel",   command=self.destroy).pack(side="left", padx=5)

    def _on_type_change(self, _event=None):
        lbl = self.EXTRA_LBL.get(self._type_var.get(), "Extra") + ":"
        self._extra_lbl_var.set(lbl)

    def _ok(self):
        # Validate
        title = self._title.get().strip()
        if not title:
            messagebox.showerror("Validation", "Title cannot be empty.", parent=self)
            return
        try:
            priority = int(self._priority.get())
            deadline = datetime.strptime(self._deadline.get().strip(), "%Y-%m-%d %H:%M")
            duration = float(self._duration.get().strip())
        except ValueError as e:
            messagebox.showerror("Validation", f"Invalid input:\n{e}", parent=self)
            return

        type_map = {"Study": TaskType.STUDY, "Exam": TaskType.EXAM, "Break": TaskType.BREAK}
        key_map  = {"Study": "subject",      "Exam": "course",      "Break": "activity"}
        t_str    = self._type_var.get()

        self.result = {
            "task_type":   type_map[t_str],
            "title":       title,
            "priority":    priority,
            "deadline":    deadline,
            "duration":    duration,
            key_map[t_str]: self._extra.get().strip() or t_str,
        }
        self.destroy()


# ═══════════════════════════════════════════════════════════════════════════
# EditTaskDialog  –  modal form for editing an existing task
# ═══════════════════════════════════════════════════════════════════════════

class EditTaskDialog(tk.Toplevel):
    """Pre-fills fields with current task values; user changes only what they want."""

    def __init__(self, parent, task):
        super().__init__(parent)
        self.title(f"Edit Task #{task.task_id}")
        self.resizable(False, False)
        self.grab_set()
        self.result = None
        self._task  = task
        self._build()
        self.wait_window()

    def _build(self):
        pad = {"padx": 10, "pady": 5}
        f   = ttk.Frame(self, padding=10)
        f.pack(fill="both", expand=True)

        ttk.Label(f, text="Title:").grid(row=0, column=0, sticky="w", **pad)
        self._title = ttk.Entry(f, width=30)
        self._title.insert(0, self._task.title)
        self._title.grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(f, text="Priority (1-5):").grid(row=1, column=0, sticky="w", **pad)
        self._priority = ttk.Spinbox(f, from_=1, to=5, width=5)
        self._priority.set(self._task.priority)
        self._priority.grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(f, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=2, column=0, sticky="w", **pad)
        self._deadline = ttk.Entry(f, width=20)
        self._deadline.insert(0, self._task.deadline_str())
        self._deadline.grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(f, text="Duration (hours):").grid(row=3, column=0, sticky="w", **pad)
        self._duration = ttk.Entry(f, width=8)
        self._duration.insert(0, str(self._task.duration))
        self._duration.grid(row=3, column=1, sticky="w", **pad)

        btn_f = ttk.Frame(f)
        btn_f.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_f, text="Save Changes", command=self._ok).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Cancel",       command=self.destroy).pack(side="left", padx=5)

    def _ok(self):
        try:
            priority = int(self._priority.get())
            deadline = datetime.strptime(self._deadline.get().strip(), "%Y-%m-%d %H:%M")
            duration = float(self._duration.get().strip())
        except ValueError as e:
            messagebox.showerror("Validation", f"Invalid input:\n{e}", parent=self)
            return
        self.result = {
            "title":    self._title.get().strip() or None,
            "priority": priority,
            "deadline": deadline,
            "duration": duration,
        }
        self.destroy()


# ═══════════════════════════════════════════════════════════════════════════
# StudyPlannerGUI  –  main window
# ═══════════════════════════════════════════════════════════════════════════

class StudyPlannerGUI:
    """
    Main Tkinter application window.

    Follows the same role as ui/cli.py:
      - Presentation only
      - Delegates ALL logic to StudyPlanner.get_instance()
      - Registers itself as an Observer via GUINotifier
    """

    # Treeview column definitions: (id, heading, width, anchor)
    COLUMNS = [
        ("id",       "#",         40,  "center"),
        ("type",     "Type",      70,  "center"),
        ("title",    "Title",     220, "w"),
        ("priority", "Priority",  65,  "center"),
        ("deadline", "Deadline",  140, "center"),
        ("duration", "Duration",  70,  "center"),
        ("status",   "Status",    100, "center"),
    ]

    STRATEGIES = {
        "By Priority (default)": SortByPriority(),
        "By Deadline":           SortByDeadline(),
        "By Duration":           SortByDuration(),
    }

    STATUS_OPTIONS = {
        "Pending":     TaskStatus.PENDING,
        "In Progress": TaskStatus.IN_PROGRESS,
        "Done":        TaskStatus.DONE,
    }

    # Row tag colours by status
    TAG_COLOURS = {
        "Pending":     ("#1a1a2e", "#e8e8f0"),
        "In Progress": ("#1a2a1a", "#b8f0b8"),
        "Done":        ("#1a1a1a", "#888899"),
    }

    def __init__(self):
        # ── Singleton planner ──────────────────────────────────────────────
        self._planner = StudyPlanner.get_instance()

        # ── Observers ─────────────────────────────────────────────────────
        self._log = LogNotifier()
        self._planner.register_observer(ConsoleNotifier())
        self._planner.register_observer(self._log)
        # GUINotifier registered after window is built (needs StringVar)

        # ── Build window ───────────────────────────────────────────────────
        self._root = tk.Tk()
        self._root.title("🎓 Smart Study Planner")
        self._root.geometry("860x560")
        self._root.minsize(720, 420)
        self._root.configure(bg="#12121e")

        self._apply_theme()
        self._status_var = tk.StringVar(value="Ready.")
        self._gui_notifier = GUINotifier(self._status_var)
        self._planner.register_observer(self._gui_notifier)

        self._build_ui()
        self._refresh_table()

    # ── Theme ──────────────────────────────────────────────────────────────
    def _apply_theme(self):
        style = ttk.Style(self._root)
        style.theme_use("clam")

        bg, fg, accent = "#12121e", "#e8e8f0", "#7c6af7"
        entry_bg = "#1e1e34"
        sel_bg   = "#3a3a6a"

        style.configure(".",              background=bg, foreground=fg,
                        font=("Segoe UI", 10))
        style.configure("TFrame",         background=bg)
        style.configure("TLabel",         background=bg, foreground=fg)
        style.configure("TButton",        background=accent, foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"), relief="flat", padding=6)
        style.map("TButton",
                  background=[("active", "#9b8cff"), ("pressed", "#5a4cc7")])
        style.configure("Danger.TButton", background="#c0392b", foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Danger.TButton",
                  background=[("active", "#e74c3c")])
        style.configure("TCombobox",      fieldbackground=entry_bg,
                        background=entry_bg, foreground=fg,
                        selectbackground=sel_bg)
        style.configure("TSpinbox",       fieldbackground=entry_bg,
                        background=entry_bg, foreground=fg)
        style.configure("TEntry",         fieldbackground=entry_bg,
                        foreground=fg, insertcolor=fg)

        # Treeview
        style.configure("Treeview",
                        background="#1a1a2e", foreground=fg,
                        fieldbackground="#1a1a2e", rowheight=28,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#2a2a4a", foreground=accent,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview",
                  background=[("selected", sel_bg)],
                  foreground=[("selected", "#ffffff")])

        style.configure("Status.TLabel",
                        background="#0d0d1a", foreground="#a0a0c0",
                        font=("Segoe UI", 9), padding=(8, 4))

    # ── UI layout ──────────────────────────────────────────────────────────
    def _build_ui(self):
        root = self._root

        # ── Header bar ────────────────────────────────────────────────────
        hdr = ttk.Frame(root)
        hdr.pack(fill="x", padx=12, pady=(12, 4))

        ttk.Label(hdr, text="🎓  Smart Study Planner",
                  font=("Segoe UI", 16, "bold"),
                  foreground="#7c6af7").pack(side="left")

        # Strategy dropdown (right side of header)
        strat_f = ttk.Frame(hdr)
        strat_f.pack(side="right")
        ttk.Label(strat_f, text="Schedule by:").pack(side="left", padx=(0, 6))
        self._strat_var = tk.StringVar(value="By Priority (default)")
        cb = ttk.Combobox(strat_f, textvariable=self._strat_var,
                          values=list(self.STRATEGIES), state="readonly", width=22)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", self._on_strategy_change)

        # ── Toolbar ────────────────────────────────────────────────────────
        toolbar = ttk.Frame(root)
        toolbar.pack(fill="x", padx=12, pady=4)

        ttk.Button(toolbar, text="＋  Add Task",
                   command=self._cmd_add).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="✏  Edit Task",
                   command=self._cmd_edit).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="🗑  Delete",
                   style="Danger.TButton",
                   command=self._cmd_delete).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="🔄  Update Status",
                   command=self._cmd_update_status).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="📥  Import Calendar",
                   command=self._cmd_import).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="📜  Event Log",
                   command=self._cmd_show_log).pack(side="right")

        # ── Separator ─────────────────────────────────────────────────────
        ttk.Separator(root, orient="horizontal").pack(fill="x", padx=12, pady=2)

        # ── Task table (Treeview) ──────────────────────────────────────────
        table_f = ttk.Frame(root)
        table_f.pack(fill="both", expand=True, padx=12, pady=4)

        cols = [c[0] for c in self.COLUMNS]
        self._tree = ttk.Treeview(table_f, columns=cols, show="headings",
                                  selectmode="browse")

        for col_id, heading, width, anchor in self.COLUMNS:
            self._tree.heading(col_id, text=heading)
            self._tree.column(col_id, width=width, anchor=anchor, minwidth=40)

        # Configure status colour tags
        for status_str, (row_bg, row_fg) in self.TAG_COLOURS.items():
            self._tree.tag_configure(status_str, background=row_bg, foreground=row_fg)

        # Scrollbar
        vsb = ttk.Scrollbar(table_f, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Double-click → edit
        self._tree.bind("<Double-1>", lambda _e: self._cmd_edit())

        # ── Status bar ─────────────────────────────────────────────────────
        ttk.Separator(root, orient="horizontal").pack(fill="x", padx=0, pady=0)
        ttk.Label(root, textvariable=self._status_var,
                  style="Status.TLabel").pack(fill="x", side="bottom")

    # ── Table refresh ──────────────────────────────────────────────────────
    def _refresh_table(self):
        """Reload all rows from the planner using the active strategy."""
        for row in self._tree.get_children():
            self._tree.delete(row)

        for task in self._planner.get_schedule():
            overdue = " 🚨" if task.is_overdue() else ""
            tag     = task.status.value          # e.g. "Pending"
            self._tree.insert("", "end", iid=str(task.task_id), tags=(tag,),
                               values=(
                                   task.task_id,
                                   task.task_type.value,
                                   task.title,
                                   task.priority,
                                   task.deadline_str() + overdue,
                                   f"{task.duration}h",
                                   task.status.value,
                               ))

    # ── Helper: get selected task ──────────────────────────────────────────
    def _selected_task(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return None
        task_id = int(sel[0])
        return self._planner.get_task(task_id)

    # ── Commands ───────────────────────────────────────────────────────────
    def _cmd_add(self):
        dlg = AddTaskDialog(self._root)
        if dlg.result:
            data = dlg.result
            tt   = data.pop("task_type")
            self._planner.add_task(tt, **data)
            self._refresh_table()

    def _cmd_edit(self):
        task = self._selected_task()
        if task is None:
            return
        dlg = EditTaskDialog(self._root, task)
        if dlg.result:
            self._planner.edit_task(task.task_id, **dlg.result)
            self._refresh_table()

    def _cmd_delete(self):
        task = self._selected_task()
        if task is None:
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete task #{task.task_id}: '{task.title}'?"):
            self._planner.delete_task(task.task_id)
            self._refresh_table()

    def _cmd_update_status(self):
        task = self._selected_task()
        if task is None:
            return

        dlg = tk.Toplevel(self._root)
        dlg.title("Update Status")
        dlg.resizable(False, False)
        dlg.grab_set()

        ttk.Label(dlg, text=f"Task #{task.task_id}: {task.title}",
                  font=("Segoe UI", 10, "bold"),
                  padding=(14, 10, 14, 4)).pack()

        var = tk.StringVar(value=task.status.value)
        for label in self.STATUS_OPTIONS:
            ttk.Radiobutton(dlg, text=label, variable=var,
                            value=label).pack(anchor="w", padx=20, pady=2)

        def apply():
            new_status = self.STATUS_OPTIONS[var.get()]
            self._planner.update_status(task.task_id, new_status)
            self._refresh_table()
            dlg.destroy()

        btn_f = ttk.Frame(dlg, padding=(14, 8))
        btn_f.pack()
        ttk.Button(btn_f, text="Apply",  command=apply).pack(side="left", padx=4)
        ttk.Button(btn_f, text="Cancel", command=dlg.destroy).pack(side="left", padx=4)
        dlg.wait_window()

    def _cmd_import(self):
        cal      = CalendarSystem()
        adapter  = TaskImportAdapter(cal)
        imported = adapter.get_tasks()
        for t in imported:
            self._planner.add_existing_task(t)
        self._refresh_table()
        messagebox.showinfo("Import Complete",
                            f"✅  {len(imported)} tasks imported from CalendarSystem.")

    def _on_strategy_change(self, _event=None):
        strategy = self.STRATEGIES[self._strat_var.get()]
        self._planner.set_strategy(strategy)
        self._refresh_table()

    def _cmd_show_log(self):
        """Open a scrollable window showing the full LogNotifier event log."""
        win = tk.Toplevel(self._root)
        win.title("Event Log")
        win.geometry("640x380")

        ttk.Label(win, text="Observer Event Log (LogNotifier)",
                  font=("Segoe UI", 11, "bold"),
                  padding=(10, 8)).pack(anchor="w")
        ttk.Separator(win).pack(fill="x")

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        txt = tk.Text(frame, font=("Consolas", 9), wrap="none",
                      bg="#0d0d1a", fg="#a0e0a0", insertbackground="#a0e0a0",
                      relief="flat", state="normal")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)

        if self._log.logs:
            txt.insert("end", "\n".join(self._log.logs))
        else:
            txt.insert("end", "(No events recorded yet.)")
        txt.configure(state="disabled")

    # ── Main loop ──────────────────────────────────────────────────────────
    def run(self):
        """Start the Tkinter event loop."""
        self._root.mainloop()
