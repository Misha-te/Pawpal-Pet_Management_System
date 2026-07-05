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

# 4. Give the pets to John
johnte.add_pet(kyle)
johnte.add_pet(emmy)

# 5. Build and print today's schedule
schedule = Schedule(owner=johnte)
schedule.generate()
print(schedule.explain())
