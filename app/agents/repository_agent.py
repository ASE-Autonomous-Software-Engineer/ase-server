from pathlib import Path

from app.runtime.event_bus import (
    EventBus
)

from app.runtime.task_store import (
    TaskStore
)

from app.observability.execution_logger import (
    ExecutionLogger
)

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    "dist",
    "build"
}

async def repository_analysis_node(state):

    # --------------------------------
    # NODE STARTED
    # --------------------------------

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "repository_analysis",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "repository_analysis",
        "running"
    )

    TaskStore.add_timeline_event(
        state["task_id"],
        {
            "node": "repository_analysis",
            "status": "running"
        }
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Starting repository indexing..."
    )

    # --------------------------------
    # REPOSITORY ANALYSIS
    # --------------------------------

    repo_path = Path(
        state["repository_path"]
    )

    repository_map = []

    for path in repo_path.rglob("*"):

        if any(
            part in IGNORED_DIRS
            for part in path.parts
        ):
            continue

        if path.is_file():

            repository_map.append({
                "file": str(path),
                "extension": path.suffix,
                "size": path.stat().st_size
            })

    state["repository_map"] = repository_map

    # --------------------------------
    # LOG RESULTS
    # --------------------------------

    await ExecutionLogger.log(
        state["task_id"],
        f"Indexed {len(repository_map)} files"
    )

    # --------------------------------
    # NODE COMPLETED
    # --------------------------------

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "repository_analysis",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "repository_analysis",
        "completed"
    )

    TaskStore.add_timeline_event(
        state["task_id"],
        {
            "node": "repository_analysis",
            "status": "completed"
        }
    )

    return state