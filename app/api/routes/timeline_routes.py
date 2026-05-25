

from fastapi import APIRouter

from app.runtime.task_store import (
    TaskStore
)

router = APIRouter()

@router.get("/tasks/{task_id}/timeline")

async def get_timeline(
    task_id: str
):

    task = TaskStore.get_task(task_id)

    if not task:
        return {
            "error": "Task not found"
        }

    return task["timeline"]