from app.git.checkpoint_manager import (
    CheckpointManager
)

from app.runtime.event_bus import (
    EventBus
)

from app.runtime.task_store import (
    TaskStore
)

from app.observability.execution_logger import (
    ExecutionLogger
)

async def checkpoint_node(state):

    # --------------------------------
    # NODE STARTED
    # --------------------------------

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "checkpoint",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "checkpoint",
        "running"
    )

    TaskStore.add_timeline_event(
        state["task_id"],
        {
            "node": "checkpoint",
            "status": "running"
        }
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Creating git checkpoint..."
    )

    # --------------------------------
    # CREATE CHECKPOINT
    # --------------------------------

    try:

        CheckpointManager.create_checkpoint(
            repo_path=state["repository_path"],
            message=(
                f"Autonomous checkpoint "
                f"for task {state['task_id']}"
            )
        )

        await ExecutionLogger.log(
            state["task_id"],
            "Checkpoint created successfully"
        )

    except Exception as e:

        # -----------------------------
        # FAILURE HANDLING
        # -----------------------------

        await ExecutionLogger.log(
            state["task_id"],
            f"Checkpoint failed: {str(e)}",
            level="ERROR"
        )

        TaskStore.update_workflow(
            state["task_id"],
            "checkpoint",
            "failed"
        )

        TaskStore.add_timeline_event(
            state["task_id"],
            {
                "node": "checkpoint",
                "status": "failed"
            }
        )

        await EventBus.emit({
            "task_id": state["task_id"],
            "node": "checkpoint",
            "status": "failed",
            "error": str(e)
        })

        state["tests_failed"] = True

        return state

    # --------------------------------
    # NODE COMPLETED
    # --------------------------------

    TaskStore.update_workflow(
        state["task_id"],
        "checkpoint",
        "completed"
    )

    TaskStore.add_timeline_event(
        state["task_id"],
        {
            "node": "checkpoint",
            "status": "completed"
        }
    )

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "checkpoint",
        "status": "completed"
    })

    return state