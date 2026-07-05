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
1. PetInfo — the pet
Holds basic facts about a pet: name, species, and age. It's a pure data class — it doesn't do any work, it just stores information the rest of the system reads. One owner can have several of these.

2. UserInfo — the owner
Represents the pet owner and, importantly, the constraints they bring to a day: their name, how much time they have (available_minutes), their preferences, and the pets they own. Its one behavior is add_pet(), which links a PetInfo to the owner. This class is where the scheduler learns "how much time is available."

3. Task — one care action
Represents a single thing that needs to happen — a walk, a feeding, meds. It stores title, duration_minutes, priority, and pet_name (which pet the task is for). Its one method, priority_score(), converts the text priority ("high"/"medium"/"low") into a number so tasks can be ranked and sorted. Like PetInfo, it's mostly a data holder, but it owns the small rule of how to score itself.

4. Schedule — the planner (the brains)
This is the only class that does real logic. It takes the owner and a list of tasks, then:

add_task() — collects the tasks to consider
generate() — chooses and orders tasks under the owner's time budget (highest priority first; among equal priority, the owner's preferred tasks first, then shorter tasks to fit more)
explain() — produces a human-readable plan and states why each task was chosen and what got skipped

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
