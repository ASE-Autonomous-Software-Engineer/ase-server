def generate_pr_summary(state):

    return f"""
    ## Autonomous Changes

    Objective:
    {state["objective"]}

    Modified Files:
    {state["target_files"]}

    Test Results:
    {state["test_results"]}
    """