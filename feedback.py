
def evaluate_task_result(task):

    successful_tasks = [
        "analyze_goals", #successfull reasoning task
        "create_plan", #successfull planing task
        "Build memory system" #successfull decomposition task

    ]

    if task["task"]in successful_tasks:

        result = {

            "task": task["task"],
            "success": True,
            "reward": 2
        }
    
    else:

        result = {
            "task": task["task"],
            "success": False,
            "reward": -1
        }

    return result