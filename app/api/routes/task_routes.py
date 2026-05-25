from fastapi import APIRouter

from app.runtime.task_store import (
    TaskStore
)

router = APIRouter()

@router.get("/tasks/{task_id}")

async def get_task(task_id: str):

    return TaskStore.get_task(
        task_id
    )

@router.get("/tasks/{task_id}/logs")

async def get_logs(task_id: str):

    task = TaskStore.get_task(
        task_id
    )

    return task.get("logs", [])

@router.get("/tasks/{task_id}/diffs")

async def get_diffs(task_id: str):

    task = TaskStore.get_task(
        task_id
    )

    return task.get("diffs", [])

@router.get("/tasks/{task_id}/timeline")

async def get_timeline(task_id: str):

    task = TaskStore.get_task(
        task_id
    )

    return task.get("timeline", [])

@router.get("/tasks/{task_id}/workflow")

async def get_workflow(task_id: str):

    task = TaskStore.get_task(
        task_id
    )

    return task.get("workflow", {})