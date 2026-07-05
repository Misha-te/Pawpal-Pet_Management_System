# PawPal+ Project Reflection

## 1. System Design
- These are some of the actions that a user of this system can excute in the app:
   1. Enter their basic information and their pets information.
   2. Add or edit tasks for example feeding the pet
   3. Generate a summary of the daily schedule.
   
**a. Initial design**

- Briefly describe your initial UML design.

 - My initial UML design has four classes. PetInfo and UserInfo store the pet's and owner's basic information, with UserInfo also holding the owner's available time and preferences. Task represents a single care action with a title, duration, and priority. Schedule is the planning class that holds the tasks and contains the scheduling logic (generate() and explain()). The relationships are: one UserInfo owns many PetInfo objects, and one Schedule contains many Task objects and plans for one UserInfo. I split the design so the first three classes just hold data while Schedule does all the decision-making.

- What classes did you include, and what responsibilities did you assign to each?
1. Task — one care action
Represents a single thing that needs to happen — a walk, a feeding, meds. It stores description, duration_minutes, priority, frequency (daily/weekly/once), due_time, a completed flag, and pet_name (which pet the task is for). It has two methods: priority_score(), which converts the text priority ("high"/"medium"/"low") into a number so tasks can be ranked, and mark_complete(), which flags the task as done so the scheduler stops planning it.

2. PetInfo — the pet
Holds basic facts about a pet (name, species, age) AND owns that pet's list of tasks. Its methods let you manage those tasks: add_task() attaches a task and stamps it with the pet's name, list_tasks() returns all of them, and pending_tasks() returns only the ones that aren't done yet. So each pet is responsible for its own tasks.

3. UserInfo — the owner
Represents the pet owner and the constraints they bring to a day: their name, how much time they have (available_minutes), their preferences, and the pets they own. Its methods are add_pet(), list_pets(), and all_tasks() — which gathers every task across all the owner's pets, giving the scheduler one place to get the full list. This class is where the scheduler learns "how much time is available" and which pets exist.

4. Schedule — the scheduler (the brains)
This is the only class that does real logic, and it works across ALL of the owner's pets, not just one. Its methods:

_pending_tasks() — asks the owner for all tasks (owner.all_tasks()) and keeps only the ones that aren't completed yet
generate() — a two-phase plan: first it SELECTS which tasks fit the time budget (highest priority first; among equal priority, the owner's preferred tasks first, then shorter tasks to fit more), then it ORDERS the chosen tasks by due_time so the day reads chronologically
explain() — produces a human-readable plan and states why each task was chosen and what got skipped

**b. Design changes**

- Did your design change during implementation?

Yes. My initial design had Task and PetInfo as separate classes with no link between them.

- If yes, describe at least one change and why you made it.

The first change was creating a connection between Task and PetInfo by adding a pet_name field to Task. I made this change because, without it, there was no way to tell which pet a task belonged to — in a household with more than one pet, a task like "Feeding" or "Morning walk" was ambiguous. Adding pet_name lets the schedule show exactly which pet each task is for (e.g. "Morning walk for Mochi"). I used a simple pet_name string rather than a full PetInfo reference to keep the UI simple, accepting the tradeoff that the link isn't strictly enforced.

I then made a bigger structural change: I moved task ownership into PetInfo. Originally the Schedule held one flat list of every task; now each PetInfo owns its own tasks (add_task/list_tasks/pending_tasks) and the Schedule gathers tasks across all pets with all_tasks(). I made this change because it better matches how the real world works — tasks belong to a pet — and because it lets the scheduler genuinely work across multiple pets instead of one shared list.

I also gave Task more real behavior. I added a due_time so the plan can be ordered chronologically, a frequency field (daily/weekly/once), a completed flag, and a mark_complete() method so finished tasks drop out of future plans (the scheduler only looks at pending tasks). I removed the unused needs field from PetInfo because it was stored but never actually read by any logic — keeping it would have been dead code.

Finally, I clarified the responsibilities between Owner and Scheduler. The Owner (UserInfo) now has an all_tasks() method that provides access to every task across its pets, and the Scheduler simply asks the Owner for that list and organizes it. This keeps the roles clean: the Owner provides the data, and the Scheduler does the planning.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My scheduler makes a simplicity/speed vs. optimality tradeoff by using a greedy selection strategy. In generate(), it ranks the tasks (by priority, then the owner's preferred tasks, then shorter duration) and adds them one at a time until the time budget runs out. It never goes back to reconsider an earlier choice. This means it is not guaranteed to find the best possible combination of tasks. For example, with a 30-minute budget and three tasks — one high-priority 30-minute task and two medium 15-minute tasks — greedy picks the single high-priority task and stops, completing one task. But the two 15-minute tasks would also fit in 30 minutes and would complete two tasks. A true optimizer (a knapsack-style algorithm) might prefer that, but greedy can't see it because it commits to the high-priority task first and never backtracks.

- Why is that tradeoff reasonable for this scenario?

It is reasonable because the goal of this app is to give a pet owner a quick, sensible, and understandable daily plan, not a mathematically perfect one. The greedy approach runs in a single pass (basically just the cost of the sort) and the logic is easy to read and explain, which matters for both the user trusting the plan and for me maintaining the code. It also respects what the owner cares about most — high-priority pet care (like feeding or meds) always gets scheduled first. A full optimization algorithm would be more complex and harder to explain for only a small, occasional gain, so for a daily pet-care to-do list the greedy strategy is the right call.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
