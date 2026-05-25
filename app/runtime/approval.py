def requires_approval(state):

    risky_keywords = [
        "delete",
        "drop database",
        "remove",
        "truncate",
        "destroy"
    ]

    objective = (
        state["objective"]
        .lower()
    )

    for keyword in risky_keywords:

        if keyword in objective:
            return True

    return False