"""
main.py  (updated)
==================
Application launcher for the Smart Study Planner.

At startup the user picks:
  1 → CLI mode   (existing terminal interface, unchanged)
  2 → GUI mode   (new Tkinter interface)

Both modes share the SAME backend:
  • StudyPlanner singleton
  • TaskFactory
  • Strategy system
  • Observer system

No business logic lives here — this is routing only.
"""

import sys
import os

# Make sure project root is importable from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def select_mode() -> str:
    """Print the mode-selection banner and return '1' or '2'."""
    print("\n" + "=" * 44)
    print("   🎓  Smart Study Planner — Launcher")
    print("=" * 44)
    print("  Select Application Mode:")
    print("    1  →  CLI  (Terminal interface)")
    print("    2  →  GUI  (Tkinter window)")
    print("=" * 44)
    while True:
        choice = input("  Your choice [1/2]: ").strip()
        if choice in ("1", "2"):
            return choice
        print("  ❌  Please enter 1 or 2.")


def main() -> None:
    try:
        mode = select_mode()
    except KeyboardInterrupt:
        print("\n  Cancelled. Goodbye!\n")
        sys.exit(0)

    if mode == "1":
        # ── CLI mode ─────────────────────────────────────────
        print("\n  Launching CLI mode…\n")
        from ui.cli import run_cli
        try:
            run_cli()
        except KeyboardInterrupt:
            print("\n  Session interrupted. Goodbye!\n")

    else:
        # ── GUI mode ─────────────────────────────────────────
        print("\n  Launching GUI mode…")
        try:
            import tkinter  # quick availability check
        except ImportError:
            print("\n  ❌  Tkinter is not available in this Python installation.")
            print("  On Ubuntu/Debian: sudo apt install python3-tk")
            print("  On Windows/macOS: Tkinter is included with the standard installer.\n")
            sys.exit(1)

        from ui.gui_app import StudyPlannerGUI
        app = StudyPlannerGUI()
        app.run()


if __name__ == "__main__":
    main()
