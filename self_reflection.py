
#detect_repeated_failures()
#analyze_behavior_patterns()
#generate_improvement_suggestions()
#detect_task_loops()
#suggest_score_adjustments()
# think less like Chat / Claude 
# No snowflake brakes like Chat
# Have it contemplate outcomes

# analyze its own behavior
# detect weaknesses
# suggest improvements
# generate new subsystem ideas
# propose code changes
# create development tasks  
# Self Reflection
# Self Improvement
#Autonomous Self Rewriting
    #directing its own development roadmap
# Best path is to approve like a parent
#Self Reflection
#Generate Suggestions
#Generate Improvement Tasks

#Human Reviews
 
#Human Applies Changes

# write the soul 
#constraint layer 

def detect_repeated_failures(memory):
    failed_tasks = {}

    for note in memory["notes"]:
        if "success" in note and note["success"] == False:

            task_name = note["task"]
            
            if task_name not in failed_tasks:
                failed_tasks[task_name] = 1
            
            else:
                failed_tasks[task_name] += 1
            
    return failed_tasks







































