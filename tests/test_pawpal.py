"""Tests for PawPal+ core behaviors."""

from pawpal_system import PetInfo, Task


def test_mark_complete_changes_status():
    """Task Completion: mark_complete() should flip completed from False to True."""
    task = Task("Feeding", 10, "high")
    assert task.completed is False  # starts not done

    task.mark_complete()

    assert task.completed is True  # now marked done


def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task to a Pet should grow that pet's task list."""
    pet = PetInfo(name="Kyle", species="dog")
    assert len(pet.tasks) == 0  # no tasks yet

    pet.add_task(Task("Morning walk", 30, "high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Feeding", 10, "high"))
    assert len(pet.tasks) == 2  # count went up with each add
