# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:


```
$ python main.py
Daily plan for Johnte (55/120 min used):
  07:30 — Feeding for Kyle (10 min, daily) [priority: high]
  08:00 — Morning walk for Kyle (30 min, daily) [priority: high]
  18:00 — Litter box cleaning for Emmy (15 min, daily) [priority: medium]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

PawPal+ goes beyond a flat to-do list. The scheduler sorts, filters, detects
conflicts, and regenerates recurring tasks. Each feature and the method that
implements it is documented below (all live in `pawpal_system.py`).

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Time sorting | `time_key()` + `Schedule.generate()` | Orders the plan chronologically; handles unpadded/blank times |
| Filtering | `UserInfo.filter_tasks()` | Narrow by pet name and/or completion status |
| Conflict detection | `Schedule.detect_conflicts()` | Warns on overlapping time blocks instead of crashing |
| Recurring tasks | `Task.next_occurrence()`, `Task.mark_complete()`, `PetInfo.complete_task()` | Auto-creates the next daily/weekly instance |

### Sorting behavior

The plan is ordered by time in `Schedule.generate()`, which sorts the chosen
tasks with the `time_key()` helper. `time_key()` converts an `"HH:MM"` string
into minutes-since-midnight, so times sort numerically rather than as text.
This means an unpadded `"9:00"` correctly sorts **before** `"18:00"` (a plain
string sort would put it after), and blank/invalid times fall to the end of the
day. Task *selection* uses a separate ranking (priority, then preferred tasks,
then shorter duration); the `time_key()` sort is purely for chronological order.

### Filtering behavior

`UserInfo.filter_tasks(pet_name="", completed=None)` returns the owner's tasks
narrowed by two optional filters that combine with AND:

- `pet_name` — keep only that pet's tasks (blank = all pets)
- `completed` — `True` for done tasks, `False` for pending, `None` to ignore status

So `owner.filter_tasks(pet_name="Kyle", completed=False)` returns Kyle's pending
tasks. (`PetInfo.pending_tasks()` is the simpler per-pet, pending-only version.)

### Conflict detection logic

`Schedule.detect_conflicts()` performs a lightweight overlap check. It treats
each timed task as a block `[due_time, due_time + duration)`, sorts the timed
tasks chronologically, and flags any pair where a task starts before the
previous one finishes. It is deliberately forgiving: untimed and invalid-time
tasks are skipped, and **it never raises** — it returns a list of human-readable
warning strings (empty when there are no clashes). `Schedule.explain()` prints
these under a "Schedule conflicts:" heading. Because it works across the owner's
whole day, it catches conflicts even between tasks belonging to different pets.

### Recurring task logic

When a `"daily"` or `"weekly"` task is completed, the next occurrence is created
automatically using Python's `timedelta`:

- `Task.next_occurrence()` builds a fresh, not-yet-completed copy with the due
  date rolled forward — `"daily"` → today + 1 day, `"weekly"` → today + 7 days.
  A `"once"` task returns `None` (it does not repeat).
- `Task.mark_complete()` marks the task done and returns that next occurrence.
- `PetInfo.complete_task()` ties it together: it marks the task complete and
  automatically adds the new instance back to the pet's task list.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
