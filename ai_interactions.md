# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code (Opus 4.8) to add two stretch features to PawPal+:

1. **Data persistence** — make the app remember pets and tasks between runs by
   saving them to a `data.json` file, via `save_to_json` / `load_from_json`
   methods.
2. **User-friendly CLI output** — color-coded status indicators, emojis for
   different task types, and structured tables using a library like `tabulate`.

For both, I asked it to document what changed in `README.md`.

**What did the agent do?**

*Persistence:*

- Edited `pawpal_system.py`: added `import json` and a `DATA_FILE` constant;
  added `to_dict()` / `from_dict()` methods to `Task`, `PetInfo`, and `UserInfo`;
  and added `UserInfo.save_to_json()` and `UserInfo.load_from_json()`.
- Handled the one non-JSON field, `Task.due_date` (a `date` object), by storing
  it as an ISO string and parsing it back with `date.fromisoformat()`.
- Made `load_from_json()` return `None` when the file doesn't exist yet (first
  run) instead of crashing.
- Added `data.json` to `.gitignore` (generated runtime data).

*CLI formatting:*

- Rewrote `main.py` to print a `tabulate` grid table for the daily plan and the
  filtering checks, with helper functions `task_emoji()`, `color()`,
  `priority_cell()`, `status_badge()`, and `plan_table()`.
- Used per-task-type emojis (🚶 🍽️ ✂️ 🏥 🧹 …), ANSI color codes for
  priority (high=red / medium=yellow / low=green) and status (✅ done / ⏳
  pending), and red/dim colors for conflict and skipped sections.
- Kept all formatting in `main.py` (not `pawpal_system.py`) so the core logic
  stays presentation-free and the Streamlit app is unaffected.
- Added `tabulate>=0.9` to `requirements.txt`.

*Verification the agent ran itself:*

- Round-tripped a saved owner (including a recurring task carrying a `due_date`)
  through save → fresh load and confirmed the data came back identical, plus the
  missing-file case returned `None`.
- Ran `python main.py` to confirm the tables render and columns stay aligned.
- Ran `pytest` after each feature — the existing 2 tests still passed.

**What did you have to verify or fix manually?**

- The editor's linter flagged `import tabulate` as unresolved, but that was just
  an environment mismatch — `tabulate` is installed and the script runs fine.
- ANSI colors only show as colors in a real terminal; in the README samples they
  appear as plain text, which the agent noted in the docs.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
