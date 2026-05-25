from app.execution.docker_executor import (
    DockerExecutor
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

async def test_execution_node(state):

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "testing",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "testing",
        "running"
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Running pytest..."
    )

    result = DockerExecutor.run_in_container(
        image="python:3.11",
        command="pytest",
        working_dir=state["repository_path"]
    )

    state["test_results"] = result["logs"]

    if result["result"]["StatusCode"] != 0:

        state["tests_failed"] = True

        await ExecutionLogger.log(
            state["task_id"],
            "Tests failed",
            level="ERROR"
        )

    else:

        state["tests_failed"] = False

        await ExecutionLogger.log(
            state["task_id"],
            "Tests passed successfully"
        )

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "testing",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "testing",
        "completed"
    )

    return state