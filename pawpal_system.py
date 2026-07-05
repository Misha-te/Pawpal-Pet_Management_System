"""PawPal+ core system.

Backbone for the pet care planner. Four objects:
- Task     : one care action (data + completion behavior)
- PetInfo  : a pet, which owns its own list of tasks
- UserInfo : the owner, who owns a list of pets + brings constraints
- Schedule : the scheduler that plans across ALL of the owner's pets
"""

from dataclasses import dataclass, field

# Maps a priority label to a number the scheduler can sort by.
PRIORITY_SCORES = {"low": 1, "medium": 2, "high": 3}


def time_key(due_time: str) -> int:
    """Turn a 'HH:MM' due_time into minutes-since-midnight for sorting.

    Tolerant of missing zero-padding, so '8:00' and '08:00' sort the same
    (a plain string sort would rank '8:00' after '18:00'). Blank or invalid
    times return a large number so those tasks sort last.
    """
    try:
        hours, minutes = due_time.strip().split(":")
        h, m = int(hours), int(minutes)
    except (ValueError, AttributeError):
        return 24 * 60  # untimed / invalid → after every real time
    if 0 <= h < 24 and 0 <= m < 60:
        return h * 60 + m
    return 24 * 60


@dataclass
class Task:
    """One pet care task (e.g. a walk, feeding, meds)."""

    description: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "daily"  # e.g. "daily", "weekly", "once"
    due_time: str = ""  # e.g. "08:00"; blank means "any time"
    completed: bool = False
    pet_name: str = ""  # set automatically when added to a pet

    def priority_score(self) -> int:
        """Return a numeric score so tasks can be ranked (higher = more urgent)."""
        return PRIORITY_SCORES.get(self.priority, 0)

    def mark_complete(self) -> None:
        """Mark this task as done so the scheduler stops planning it."""
        self.completed = True


@dataclass
class PetInfo:
    """A pet, along with the care tasks that belong to it."""

    name: str
    species: str = "dog"
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet (stamps the task with the pet's name)."""
        task.pet_name = self.name
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def pending_tasks(self) -> list[Task]:
        """Return only the tasks that still need to be done."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class UserInfo:
    """The pet owner: identifying info, their pets, and daily constraints."""

    name: str
    available_minutes: int = 120
    preferences: dict = field(default_factory=dict)
    pets: list[PetInfo] = field(default_factory=list)

    def add_pet(self, pet: PetInfo) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def list_pets(self) -> list[PetInfo]:
        """Return all of the owner's pets."""
        return self.pets

    def all_tasks(self) -> list[Task]:
        """Provide access to every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.list_tasks()]

    def filter_tasks(self, pet_name: str = "", completed: bool = None) -> list[Task]:
        """Return tasks narrowed by pet name and/or completion status.

        Both filters are optional and combine (AND):
        - pet_name: keep only tasks for that pet (blank = all pets)
        - completed: keep only done tasks (True) or pending ones (False);
          None means don't filter on status.
        """
        tasks = self.all_tasks()
        if pet_name:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks


@dataclass
class Schedule:
    """Builds and explains a daily plan across ALL of the owner's pets.

    This is where the scheduling logic lives. It gathers tasks from every
    pet the owner has, then chooses and orders them under the time budget.
    """

    owner: UserInfo
    plan: list[Task] = field(default_factory=list)

    def _pending_tasks(self) -> list[Task]:
        """Ask the owner for all tasks, then keep only the ones not done yet."""
        return [t for t in self.owner.all_tasks() if not t.completed]

    def _is_preferred(self, task: Task) -> bool:
        """True if the task matches one of the owner's preferred keywords.

        The owner sets preferences like {"prefer": ["walk", "meds"]}; any
        task whose description contains a keyword is treated as preferred.
        """
        prefer = self.owner.preferences.get("prefer", [])
        return any(kw.lower() in task.description.lower() for kw in prefer)

    def generate(self) -> list[Task]:
        """Choose and order tasks that fit within the owner's available time.

        Two-phase strategy:
        1. SELECT what fits: rank tasks by priority, then the owner's
           preferred tasks, then shorter tasks (to fit more), and keep
           adding until the time budget runs out.
        2. ORDER for the day: sort the chosen tasks by their due_time so the
           final plan reads chronologically (untimed tasks go last).
        """
        remaining = self.owner.available_minutes

        ranked = sorted(
            self._pending_tasks(),
            key=lambda t: (
                -t.priority_score(),
                0 if self._is_preferred(t) else 1,
                t.duration_minutes,
            ),
        )

        chosen = []
        for task in ranked:
            if task.duration_minutes <= remaining:
                chosen.append(task)
                remaining -= task.duration_minutes

        self.plan = sorted(chosen, key=lambda t: time_key(t.due_time))
        return self.plan

    def explain(self) -> str:
        """Return a human-readable summary of the plan and why it was chosen."""
        if not self.plan:
            return "No plan generated yet. Call generate() first."

        used = sum(t.duration_minutes for t in self.plan)
        lines = [
            f"Daily plan for {self.owner.name} "
            f"({used}/{self.owner.available_minutes} min used):",
        ]
        for task in self.plan:
            when = f"{task.due_time} — " if task.due_time else ""
            who = f" for {task.pet_name}" if task.pet_name else ""
            star = " (preferred)" if self._is_preferred(task) else ""
            lines.append(
                f"  {when}{task.description}{who} "
                f"({task.duration_minutes} min, {task.frequency}) "
                f"[priority: {task.priority}]{star}"
            )

        chosen = set(id(t) for t in self.plan)
        skipped = [t for t in self._pending_tasks() if id(t) not in chosen]
        if skipped:
            lines.append("Skipped (not enough time):")
            for task in skipped:
                lines.append(
                    f"  - {task.description} ({task.duration_minutes} min)"
                )

        return "\n".join(lines)


if __name__ == "__main__":
    owner = UserInfo(
        name="Jordan",
        available_minutes=60,
        preferences={"prefer": ["walk"]},
    )

    mochi = PetInfo(name="Mochi", species="cat", age=3)
    mochi.add_task(Task("Morning walk", 30, "high", due_time="08:00"))
    mochi.add_task(Task("Feeding", 10, "high", due_time="07:30"))
    mochi.add_task(Task("Grooming", 25, "low", frequency="weekly", due_time="18:00"))

    biscuit = PetInfo(name="Biscuit", species="dog", age=5)
    biscuit.add_task(Task("Enrichment play", 15, "medium", due_time="16:00"))
    already_fed = Task("Feeding", 10, "high", due_time="07:45")
    already_fed.mark_complete()  # done earlier — scheduler should skip it
    biscuit.add_task(already_fed)

    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    schedule = Schedule(owner=owner)
    schedule.generate()
    print(schedule.explain())
