import json
import datetime
import random

thought_types = [
    "analyze",
    "idea",
    "task",
    "evaluate",
    "question"
]

actions = [
    "search_memory",
    "log_progress",
    "refine_goal",
    "do_nothing"
]
#task = {key > Value}
task_que = [
{"task": "analyze_goal", "priority": 3},
{"task": "create_plan", "priority": 2},
{"task": "execute_task", "priority": 1}

]

thought_weights = {
    "analyze": 0.35,
    "task": 0.25, 
    "idea": 0.15,
    "evaluate": 0.15,
    "question": 0.10    
}

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

config = load_json("config.json")
goals = load_json("goals.json")
memory = load_json("memory.json")


print("SYSTEM CONFIG:")
print(config)

print("\nCURRENT GOAL:")
print(goals)

print("\nMEMORY STATE:")
print(memory)

print("\n--- AI KERNEL START ---")

thinking_mode = config["thinking_mode"] #manual switch no longer thinking pulled up in config

def decide_action(thought):
    if thought == "analyze":
        return "search_memory"
    elif thought == "idea":
        return "refine_goal"
    elif thought == "task":
        return "log_progress"
    elif thought == "evaluate":
        return "search_memory"
    elif thought == "question":
        return "do_nothing"
    
def refine_goal(current_goal):
    print("Refining goal logic activated...")
    new_goal = current_goal + "(refined)"
    return new_goal

def score_thought(thought, goal, memory, remaining_budget):
    score = 0 

    if thought == "task":
        score += 5
    elif thought == "analyze":
        score += 3
    if remaining_budget <= 5 and thought == "task":
        score += 3 
    if "refined" in goal and thought == "evaluate":
        score += 2 
    recent = recent_thoughts(memory) #call thoughts

    if recent.count(thought) >= 2: #how many times though appears if it show up two or more times
        score -= 4 # if it does show up take away four points does something multiple times says stop it scor

    return score

def is_progress_made(memory): #learn
    # check if anything new was learned or changed
    notes = memory["notes"]
    recent = notes[-3:] #learn
    
    for note in recent:  #learn
        if note.get("event") == "progress_logged":
            return True
    return False    # learn why is outside the loop instead of under if i checked all notes and found nothing return false becuase there is no event in the notes

    
          # false and not 

def recent_thoughts(memory, n=3):
    thoughts = [note["thought"] for note in memory["notes"] if "thought" in note]
    return thoughts[-n:]

def get_next_task(task_que):
    if not task_que:
        return None

    sorted_tasks = sorted(task_que, key=lambda x: x["priority"], reverse=True) #learn this line more

    return sorted_tasks[0]

def execute_task(task):
    if task["task"] == "analyze_goal": #learn how does it know how to look in dictionary it doesnt say task_que
        print("Executing: analyzing goal deeply...")

    elif task["task"] =="create_plan":
        print("Executing: creating a plan...")
    
    elif task["task"] == "execute_task":
        print("Executing: performing a real task...")

def remove_task(task_que, task):
    task_que.remove(task)

for step in range(config["max_steps"]):
    remaining_budget = config["budget_limit"] - step

    # build scores dynamically using the scoring function
    thought_score_map = {}
    for t in thought_types:
        thought_score_map[t] = score_thought(
            t,
            goal=goals["current_goal"],
            memory=memory,
            remaining_budget=remaining_budget
        )


    print(f"\nSTEP {step+1}:")

    goal = goals["current_goal"]

    print("Current Goal:", goal)
    print("Remaining Budget:", remaining_budget)

    current_task = get_next_task(task_que)

    if current_task: 
        print("Current Task:", current_task)
        execute_task(current_task)
        remove_task(task_que, current_task)
    

    if not is_progress_made(memory):
        print("No progress detected - boosting analyze score")
        thought_score_map["analyze"] += 2
    if thinking_mode == "stochastic":
        thought = random.choices(
            population=list(thought_weights.keys()),
            weights=list(thought_weights.values()),
            k=1
        )[0]
    else:
        print("THOUGHT SCORES:", thought_score_map)
        thought = max(thought_score_map, key=thought_score_map.get)

    
    print("Thought Type:", thought)


    if remaining_budget <= 5:
        print("Low budget mode activated (score influence only)")
        thought_score_map["task"] += 3
        thought = max(thought_score_map, key=thought_score_map.get)


    action = decide_action(thought)
    print("Chosen Action:", action)

    if action == "search_memory":
        for note in memory["notes"]:
            print("\n----------")
            if "step" in note:
                print(f"STEP {note['step']}")
            print(note)
        print("reviewing past observations...")
    
    if action == "log_progress":
        print("Logging progress into memory...")
        memory["notes"].append({
            "event": "progress_logged",
            "time": datetime.datetime.now().isoformat()
        })
    if action == "refine_goal":
        print("AI is refining its goal...")
        goals["current_goal"] = refine_goal(goals["current_goal"])
    


    if thought == "analyze":
        print("Analyzing the goal...")
    elif thought == "idea":
        print("Generating  a new idea...")
    elif thought == "task":
        print("Creating a task...")

        if "analyze" in recent_thoughts(memory):
            new_task = {"task": "create_plan", "priority": 2}
        else:
            new_task = {"task": "analyze_goal", "priority": 2}
        
        task_que.append(new_task)
        print("New task added:", new_task)


    elif thought == "evaluate":
        print("Evaluating progress...")
    elif thought == "question":
        print("Asking a question about the goal...")

    observation = {

        "step": step + 1,
        "goal": goal,
        "thought": thought,
        "score": thought_score_map.get(thought, None),
        "time": datetime.datetime.now().isoformat()
    }

    memory["notes"].append(observation)

print("\nUPDATED MEMORY:")
print(memory)
save_json("memory.json", memory)


