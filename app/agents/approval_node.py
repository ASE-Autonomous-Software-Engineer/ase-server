from app.runtime.approval_rules import (
    requires_approval
)

from app.runtime.event_bus import (
    EventBus
)

from app.runtime.task_store import (
    TaskStore
)

async def approval_node(state):

    # -----------------------------
    # CHECK IF APPROVAL REQUIRED
    # -----------------------------

    approval_required = (
        requires_approval(state)
    )

    # -----------------------------
    # AUTO APPROVE SAFE TASKS
    # -----------------------------

    if not approval_required:

        state["awaiting_approval"] = False

        state["approval_status"] = (
            "auto-approved"
        )

        return state

    # -----------------------------
    # REQUIRE HUMAN APPROVAL
    # -----------------------------

    state["awaiting_approval"] = True

    state["approval_status"] = (
        "pending"
    )

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "approval",
        "status": "awaiting"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "approval",
        "awaiting"
    )

    return state