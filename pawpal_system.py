"""PawPal+ core system.

Backbone for the pet care planner. Four objects:
- PetInfo   : the pet (data)
- UserInfo  : the owner + their constraints (data)
- Task      : one care action (data)
- Schedule  : the planner that turns tasks into a daily plan (logic)
"""

from dataclasses import dataclass, field

# Maps a priority label to a number the scheduler can sort by.
PRIORITY_SCORES = {"low": 1, "medium": 2, "high": 3}


@dataclass
class PetInfo:
    """Basic info about a pet."""

    name: str
    species: str = "dog"
    age: int = 0
    needs: list[str] = field(default_factory=list)


@dataclass
class UserInfo:
    """The pet owner and the constraints they bring to a day."""

    name: str
    available_minutes: int = 120
    preferences: dict = field(default_factory=dict)
    pets: list[PetInfo] = field(default_factory=list)

    def add_pet(self, pet: PetInfo) -> None:
        self.pets.append(pet)


@dataclass
class Task:
    """One pet care task (e.g. a walk, feeding, meds)."""

    title: str
    duration_minutes: int
    priority: str = "medium"

    def priority_score(self) -> int:
        """Return a numeric score so tasks can be ranked (higher = more urgent)."""
        return PRIORITY_SCORES.get(self.priority, 0)


@dataclass
class Schedule:
    """Builds and explains a daily plan from a list of tasks.

    This is where the scheduling logic lives.
    """

    owner: UserInfo
    tasks: list[Task] = field(default_factory=list)
    plan: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def generate(self) -> list[Task]:
        """Choose and order tasks that fit within the owner's available time.

        Strategy: highest priority first; among equal priority, shorter
        tasks first (so we can fit more of them). Skip any task that would
        blow the time budget.
        """
        self.plan = []
        remaining = self.owner.available_minutes

        ranked = sorted(
            self.tasks,
            key=lambda t: (-t.priority_score(), t.duration_minutes),
        )

        for task in ranked:
            if task.duration_minutes <= remaining:
                self.plan.append(task)
                remaining -= task.duration_minutes

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
        for i, task in enumerate(self.plan, start=1):
            lines.append(
                f"  {i}. {task.title} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )

        skipped = [t for t in self.tasks if t not in self.plan]
        if skipped:
            lines.append("Skipped (not enough time):")
            for task in skipped:
                lines.append(f"  - {task.title} ({task.duration_minutes} min)")

        return "\n".join(lines)


if __name__ == "__main__":
    owner = UserInfo(name="Jordan", available_minutes=60)
    owner.add_pet(PetInfo(name="Mochi", species="cat", age=3))

    schedule = Schedule(owner=owner)
    schedule.add_task(Task("Morning walk", 30, "high"))
    schedule.add_task(Task("Feeding", 10, "high"))
    schedule.add_task(Task("Grooming", 25, "low"))
    schedule.add_task(Task("Enrichment play", 15, "medium"))

    schedule.generate()
    print(schedule.explain())
