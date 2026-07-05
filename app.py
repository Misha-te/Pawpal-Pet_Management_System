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

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    due_time = st.text_input("Due (HH:MM)", value="08:00")

if st.button("Add task"):
    # Build a real Task object from the inputs and remember it across reruns.
    st.session_state.tasks.append(
        Task(task_title, int(duration), priority, due_time=due_time)
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
        schedule.generate()

        st.success("Here's today's plan:")
        st.text(schedule.explain())
