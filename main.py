"""
main.py
=======
Application entry point for the Smart Study Planner.

Run this file to launch the interactive CLI:
    python main.py

All the design patterns wire together through the CLI → StudyPlanner path.
"""

import sys
import os

# Ensure the project root is on the Python path so imports resolve correctly
# when the script is run from any working directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.cli import run_cli


def main() -> None:
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n  Session interrupted. Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
