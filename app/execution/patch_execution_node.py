from app.execution.patch_parser import (
    PatchParser
)

from app.execution.autonomus_executor import (
    AutonomousExecutor
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

async def patch_execution_node(state):

    # --------------------------------
    # NODE STARTED
    # --------------------------------

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "patch_execution",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "patch_execution",
        "running"
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Applying generated patches..."
    )

    # --------------------------------
    # PARSE PATCH RESPONSE
    # --------------------------------

    parsed = PatchParser.parse(
        state["generated_code"]
    )

    if "files" not in parsed:

        state["tests_failed"] = True

        await ExecutionLogger.log(
            state["task_id"],
            "Patch parsing failed",
            level="ERROR"
        )

        return state

    # --------------------------------
    # APPLY PATCHES
    # --------------------------------

    for file_patch in parsed["files"]:

        result = AutonomousExecutor.execute_patch(
            task_id=state["task_id"],
            file_path=file_patch["file_path"],
            updated_content=file_patch[
                "updated_content"
            ]
        )

        await ExecutionLogger.log(
            state["task_id"],
            f"Patched file: {file_patch['file_path']}"
        )

    # --------------------------------
    # NODE COMPLETED
    # --------------------------------

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "patch_execution",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "patch_execution",
        "completed"
    )

    return state