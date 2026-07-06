"""Demo script for PawPal+.

Builds an owner with two pets and a few tasks, then prints today's schedule
as a colorful, emoji-annotated CLI report using the `tabulate` library.
"""

from tabulate import tabulate

from pawpal_system import UserInfo, PetInfo, Task, Schedule

# --- Presentation helpers -------------------------------------------------
# These live in the CLI (not in pawpal_system.py) so the core logic stays
# free of terminal formatting — the Streamlit app renders its own way.

# ANSI color codes for the terminal. RESET returns text to the default color.
RESET = "\033[0m"
COLORS = {
    "red": "\033[91m",
    "yellow": "\033[93m",
    "green": "\033[92m",
    "cyan": "\033[96m",
    "dim": "\033[90m",
    "bold": "\033[1m",
}

# Map a priority to a color so urgency is visible at a glance.
PRIORITY_COLORS = {"high": "red", "medium": "yellow", "low": "green"}

# Keyword → emoji, so each task type gets a recognizable icon. Checked in
# order, so more specific words come first.
TASK_EMOJIS = [
    ("walk", "🚶"),
    ("feed", "🍽️"),
    ("groom", "✂️"),
    ("vet", "🏥"),
    ("litter", "🧹"),
    ("play", "🎾"),
    ("enrich", "🎾"),
    ("med", "💊"),
    ("train", "🎓"),
    ("bath", "🛁"),
]


def color(text: str, name: str) -> str:
    """Wrap text in an ANSI color so it prints colored in the terminal."""
    return f"{COLORS.get(name, '')}{text}{RESET}"


def task_emoji(description: str) -> str:
    """Pick an emoji for a task based on keywords in its description."""
    text = description.lower()
    for keyword, emoji in TASK_EMOJIS:
        if keyword in text:
            return emoji
    return "🐾"  # default paw print for anything unrecognized


def priority_cell(priority: str) -> str:
    """Return the priority label color-coded by urgency (high=red, low=green)."""
    return color(priority.upper(), PRIORITY_COLORS.get(priority, "dim"))


def status_badge(completed: bool) -> str:
    """Return a color-coded ✅/⏳ badge for a task's completion status."""
    return color("✅ done", "green") if completed else color("⏳ pending", "yellow")


def plan_table(plan: list[Task]) -> str:
    """Render the daily plan as a structured grid table via tabulate."""
    rows = [
        [
            task.due_time or "anytime",
            f"{task_emoji(task.description)} {task.description}",
            task.pet_name,
            f"{task.duration_minutes} min",
            priority_cell(task.priority),
            task.frequency,
            status_badge(task.completed),
        ]
        for task in plan
    ]
    headers = ["Time", "Task", "Pet", "Duration", "Priority", "Frequency", "Status"]
    return tabulate(rows, headers=headers, tablefmt="rounded_grid")


# --- Build the demo data --------------------------------------------------

# 1. Create the owner
johnte = UserInfo(name="Johnte", available_minutes=120)

# 2. Create two pets: a dog and a cat
kyle = PetInfo(name="Kyle", species="dog", age=4)
emmy = PetInfo(name="Emmy", species="cat", age=2)

# 3. Add tasks out of order on purpose — the scheduler sorts them by time,
#    so the printed plan should come out chronological no matter the order here.
#    (Note "9:00" is intentionally unpadded to show time sorting handles it.)
emmy.add_task(Task("Litter box cleaning", 15, "medium", due_time="18:00"))
kyle.add_task(Task("Evening walk", 25, "medium", due_time="9:00"))
kyle.add_task(Task("Feeding", 10, "high", due_time="07:30"))
emmy.add_task(Task("Feeding", 10, "high", due_time="08:15"))
kyle.add_task(Task("Morning walk", 30, "high", due_time="08:00"))

# Two conflicting tasks: the 30-min vet visit at 12:00 runs until 12:30,
# but grooming is scheduled at 12:15 — the scheduler should warn about this.
kyle.add_task(Task("Vet visit", 30, "high", due_time="12:00"))
emmy.add_task(Task("Grooming", 20, "medium", due_time="12:15"))

# 4. Give the pets to John
johnte.add_pet(kyle)
johnte.add_pet(emmy)

# 5. Build today's schedule (tasks come out sorted by time)
schedule = Schedule(owner=johnte)
plan = schedule.generate()

# --- Print the colorful report -------------------------------------------

used = sum(t.duration_minutes for t in plan)
print(color(f"\n🐾 Daily plan for {johnte.name}", "bold"), end=" ")
print(color(f"({used}/{johnte.available_minutes} min used)", "cyan"))
print(plan_table(plan))

# Conflict warnings, in red so they stand out.
conflicts = schedule.detect_conflicts()
if conflicts:
    print(color("\n⚠️  Schedule conflicts:", "red"))
    for warning in conflicts:
        print("  " + color(warning.removeprefix("⚠ "), "red"))
else:
    print(color("\n✅ No time conflicts detected.", "green"))

# Tasks skipped because the time budget ran out, dimmed.
scheduled_ids = {id(t) for t in plan}
skipped = [t for t in johnte.filter_tasks(completed=False) if id(t) not in scheduled_ids]
if skipped:
    print(color("\n⏭️  Skipped (not enough time):", "dim"))
    for task in skipped:
        line = f"  {task_emoji(task.description)} {task.description} ({task.duration_minutes} min)"
        print(color(line, "dim"))

# 6. Show the filtering methods working as a small table
print(color("\n🔍 Filtering checks", "bold"))


def summarize(tasks: list[Task]) -> str:
    """Join a task list into a one-line, emoji-tagged summary."""
    parts = [f"{task_emoji(t.description)} {t.description} ({t.due_time or 'anytime'})" for t in tasks]
    return ", ".join(parts) or color("none", "dim")


filter_rows = [
    ["Kyle's tasks", summarize(johnte.filter_tasks(pet_name="Kyle"))],
    ["Emmy's tasks", summarize(johnte.filter_tasks(pet_name="Emmy"))],
    ["Pending", summarize(johnte.filter_tasks(completed=False))],
    ["Completed", summarize(johnte.filter_tasks(completed=True))],
]
print(tabulate(filter_rows, headers=["Filter", "Tasks"], tablefmt="rounded_grid"))
