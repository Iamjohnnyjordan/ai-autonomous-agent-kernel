
def decompose_goal(goal):
    goal_map = {

        "Learn controlled AI architecture":
        [
            "Build memory system",
            "Build reasoning system",
            "Build planning system",
            "Build execution system"
        ],

        "Build memory system":
        [
            "Create JSON storage",
            "Store observations",
            "Load previous memories"
        ],

        "Build reasoning engine":
        [
            "Score thoughts",
            "Evaluate decisions",
            "Prioritize actions"
        ]
    }

    return goal_map.get(goal, [])