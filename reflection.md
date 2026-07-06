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

I used AI in two main ways. First, I used it to help generate code — especially the algorithmic parts like the sorting and filtering logic, which were the pieces the project actually needed. Second, I used it to save time navigating my own code. Instead of scrolling through the whole file trying to find a specific method or line, I would just ask the AI "where is this method?" and it would point me straight to it. That let me spend my time on the logic instead of searching. I also used AI for refactoring — for example, I asked it whether there was a way to make my algorithms cleaner and more readable for a human, which helped me improve the code without changing what it does. I did not lean on AI much for brainstorming; most of the design ideas were my own, and I mainly brought AI in once I knew what I wanted to build.

- What kinds of prompts or questions were most helpful?

The most helpful prompts came from turning the assignment requirements into questions. I looked at the rubric and the requirements, and instead of just reading them, I rephrased each requirement as a direct question and used that as my prompt (for example, turning "sort tasks by time" into "how do I sort my tasks by time in the scheduler?"). This kept the AI focused on exactly what the project asked for. Specific, task-focused questions about the sorting and filtering algorithms were the most useful, along with "where is X in my code?" questions for navigation and "how can I make this more readable?" questions for cleanup.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

There were several moments where I did not accept the AI's suggestion as-is. One happened early in the coding exercise: I asked the AI to generate some code and put it in main.py, but it tried to write the code into app.py instead. Because that was not where I wanted it, I declined the change and had it target the correct file. Another kind of moment came up more than once around process: there was a step where I was supposed to review the instructions and plan first, but the AI would run ahead and start making all the edits before I had done that step myself. In those cases I stopped the AI mid-edit and rejected the suggested changes so I could stay in control of the order I worked in. These were not one-offs — it happened several times, and each time I chose to override the AI rather than just accept what it produced.

- How did you evaluate or verify what the AI suggested?

I evaluated the AI's suggestions mainly by reading the code myself. I took a Python course a few months ago, so I can generally understand Python code and tell whether what the AI wrote makes sense and does what I asked. When the AI generated something I did not understand, I did not just trust it — I asked it to explain the code to me line by line, and I would tell it to answer as if it were a software engineer or a computer science student, so the explanation was at a level I could follow. Reading the code plus asking for line-by-line explanations is how I made sure I actually understood and agreed with what was going into my project.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I wrote two tests in tests/test_pawpal.py covering the two behaviors that matter most for this app: adding a task and completing a task. The first test, test_add_task_increases_pet_task_count, adds tasks to a pet and checks that the pet's task list grows by one each time. The second test, test_mark_complete_changes_status, creates a task, confirms it starts as not completed, calls mark_complete(), and confirms its status flips to completed. Both tests pass when I run pytest.

- Why were these tests important?

These were important because tasks are the whole idea behind the app — the point of PawPal+ is to make it easier for a pet owner to schedule the care tasks their pets need. Adding tasks is the most basic thing a user does, and since a pet's tasks are essentially endless, the app has to reliably let the user keep adding more; if add_task did not grow the list correctly, nothing else in the scheduler would work. Task completion mattered for a different reason: the completed status is what tells the app whether a task is done or still pending, and that status drives the filtering feature (filter_tasks) that lets an owner see only done or only not-done tasks. Testing that mark_complete() actually changes the status gives me confidence that both the "is it finished?" logic and the filtering built on top of it are trustworthy.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am about 99.7% confident that my scheduler works correctly — borrowing the three-sigma confidence interval idea from statistics. I say this because I have run the app several times, and every single time I ran it, it worked as expected and produced a correct plan. Based on that track record, I would estimate only about a 0.3% probability of something going wrong, which is why I am not claiming 100% — there is always a small chance of an edge case I have not hit yet.

- What edge cases would you test next if you had more time?

If I had more time, the main things I would add and test are around planning ahead and sharing the plan. First, I would create an option to schedule tasks in advance for specific future dates, so the owner can plan out care beyond just today rather than only seeing the current day's plan. Testing that would mean checking that tasks land on the correct future date and that the plan for a given day only shows the tasks meant for that day. Second, I would add a feature that lets the owner download or export the daily summary (for example, to print and put on the fridge) so the schedule is easy to follow throughout the day, and I would test that the exported summary matches what the scheduler actually produced. I would also want to add more automated tests for the parts I currently verify by running the app — the time sorting (including unpadded and blank times), the conflict warnings for overlapping tasks, and the daily/weekly recurrence dates — so those behaviors are covered by tests and not just manual checks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Overall, this project went better than my first project (the Game Glitchers project). The biggest reason was the coordination and collaboration between me and the AI, which was really good this time. I got much better at writing clear prompts to implement the changes and required features, and that made the whole process smoother. Interestingly, even though this project felt bigger and a little more demanding than the previous one, it actually took me less time — which I credit to that improved collaboration and to understanding how to come up with good prompts.

In general I am happy with the final product, but the part I am most satisfied with is the tasks and their tests. I would prompt the AI to build them and then cross my fingers as I ran them in the terminal, hoping they would pass — and they did. Seeing the tests pass was really satisfying and gave me confidence in the core of the app.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would focus on the features I mentioned in the previous section: adding an option to plan ahead by scheduling tasks for specific future dates instead of only the current day, and adding a way for the owner to download or export the daily summary (for example, to print and put on the fridge) so the schedule is easier to follow. Those two additions would make the app more useful in real, everyday pet care.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that no matter how capable the AI is, the human has to stay in charge. I am the lead architect: my job is to review what the AI suggests and understand it before accepting it, rather than just taking every change it produces. On top of that, I learned that AI makes it much easier to apply the principle of abstraction, which is one of the cornerstones of object-oriented programming. The idea of abstraction is that we don't need to worry about all the low-level details happening in the background — we can focus on getting the task done without understanding 100% of how everything works underneath. Working with AI reinforced this, and it also means people with lower programming experience can still build meaningful projects, as long as they stay in control and verify the work.
