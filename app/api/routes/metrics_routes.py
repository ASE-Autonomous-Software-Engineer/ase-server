from fastapi import APIRouter

from app.runtime.task_store import (
    TaskStore
)

router = APIRouter()

@router.get("/metrics/runtime")

async def runtime_metrics():

    total_tasks = len(TaskStore.tasks)

    completed = 0

    failed = 0

    for task in TaskStore.tasks.values():

        workflow = task["workflow"]

        if "completed" in workflow.values():
            completed += 1

        if "failed" in workflow.values():
            failed += 1

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed,
        "failed_tasks": failed
    }