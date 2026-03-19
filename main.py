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

for step in range(config["max_steps"]):

    print(f"\nSTEP {step+1}:")

    goal = goals["current_goal"]

    print("Current Goal:", goal)

    thought = random.choices(
        population=list(thought_weights.keys()),
        weights=list(thought_weights.values()),
        k=1
     )[0]
    
    print("Thought Type:", thought)

    action = decide_action(thought)
    print("Chosen Action:", action)

    if action == "search_memory":
        print(memory)
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
    elif thought == "evaluate":
        print("Evauluating progress...")
    elif thought == "question":
        print("Asking a question about the goal...")

    observation = {

        "step": step + 1,
        "goal": goal,
        "thought":thought,
        "time": datetime.datetime.now().isoformat()
    }

    memory["notes"].append(observation)

print("\nUPDATED MEMORY:")
print(memory)
save_json("memory.json", memory)


