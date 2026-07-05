"""Demo script for PawPal+.

Builds an owner with two pets and a few tasks, then prints today's schedule.
"""

from pawpal_system import UserInfo, PetInfo, Task, Schedule

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

# 5. Build and print today's schedule (tasks come out sorted by time)
schedule = Schedule(owner=johnte)
schedule.generate()
print(schedule.explain())

# 6. Show the filtering methods working in the terminal
print("\n--- Filtering checks ---")


def show(label, tasks):
    """Print a labeled, one-line summary of a task list."""
    summary = ", ".join(f"{t.description} ({t.due_time or 'anytime'})" for t in tasks)
    print(f"{label}: {summary or 'none'}")


show("Kyle's tasks", johnte.filter_tasks(pet_name="Kyle"))
show("Emmy's tasks", johnte.filter_tasks(pet_name="Emmy"))
show("Pending tasks", johnte.filter_tasks(completed=False))
show("Completed tasks", johnte.filter_tasks(completed=True))
