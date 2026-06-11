# THOUGHT MEMORY ANALYSIS SECTION
# Pull recent thoughts from memory for repetition analysis

def recent_thoughts(memory, n=3):
    thoughts = [note["thought"] for note in memory["notes"] if "thought" in note]
    return thoughts[-n:]


# FEEDBACK ANALYSIS SECTION V2 
# Analyze previous feedback rewards stored in memory

def recent_rewards(memory):

    rewards = [

        note["reward"]
        for note in memory["notes"]
        if "reward" in note
    ]

    return rewards[-5:]
    #f

# THOUGHT SCORING SECTION
# Score thoughts based on heuristics, memory, and penalties
def score_thought(thought, goal, memory, remaining_budget):
    score = 0 
    # REINFORCEMENT LEARNING SECTION
    # Adjust thought scoring based on recent rewards

    recent_reward_history = recent_rewards(memory) #pull recent rewards from memory

    if sum(recent_reward_history) > 0:
        score += 1
    
    if sum(recent_reward_history) < 0:
        score -= 1
    
    

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

