import streamlit as st

from pawpal_system import UserInfo, PetInfo, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=1440, value=120
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed into your scheduler below.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    due_time = st.text_input("Due (HH:MM)", value="08:00")
with col5:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)

if st.button("Add task"):
    # Build a real Task object from the inputs and remember it across reruns.
    st.session_state.tasks.append(
        Task(task_title, int(duration), priority, frequency=frequency, due_time=due_time)
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "task": t.description,
                "minutes": t.duration_minutes,
                "priority": t.priority,
                "due": t.due_time,
                "frequency": t.frequency,
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task first.")
    else:
        # Build the object graph from the UI inputs, then run the scheduler.
        owner = UserInfo(name=owner_name, available_minutes=int(available_minutes))
        pet = PetInfo(name=pet_name, species=species)
        for task in st.session_state.tasks:
            pet.add_task(task)
        owner.add_pet(pet)

        schedule = Schedule(owner=owner)
        plan = schedule.generate()  # tasks come back sorted by time

        # Headline summary of the plan.
        used = sum(t.duration_minutes for t in plan)
        st.success(
            f"Today's plan for {owner_name}: "
            f"{len(plan)} task(s) scheduled, {used}/{int(available_minutes)} min used."
        )

        # The sorted plan, rendered as a clean table (chronological order).
        st.markdown("#### 🗓️ Today's plan (sorted by time)")
        st.table(
            [
                {
                    "time": t.due_time or "anytime",
                    "task": t.description,
                    "pet": t.pet_name,
                    "minutes": t.duration_minutes,
                    "priority": t.priority,
                    "frequency": t.frequency,
                }
                for t in plan
            ]
        )

        # Conflict warnings from the scheduler's lightweight overlap check.
        conflicts = schedule.detect_conflicts()
        if conflicts:
            st.markdown("#### ⚠️ Schedule conflicts")
            for warning in conflicts:
                st.warning(warning.removeprefix("⚠ "))
        else:
            st.info("No time conflicts detected. ✅")

        # Tasks that didn't fit the time budget (filter out the scheduled ones).
        scheduled_ids = {id(t) for t in plan}
        skipped = [
            t for t in owner.filter_tasks(completed=False) if id(t) not in scheduled_ids
        ]
        if skipped:
            st.markdown("#### ⏭️ Skipped (not enough time)")
            st.table(
                [
                    {
                        "task": t.description,
                        "minutes": t.duration_minutes,
                        "priority": t.priority,
                    }
                    for t in skipped
                ]
            )

        # Keep the full text explanation available, but tucked away.
        with st.expander("Full text explanation"):
            st.text(schedule.explain())
