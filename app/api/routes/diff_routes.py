# ============================================
# FILE: app/api/routes/diff_routes.py
# ============================================

from fastapi import APIRouter

from app.runtime.task_store import (
    TaskStore
)

router = APIRouter()

@router.get("/tasks/{task_id}/diffs")

async def get_diffs(
    task_id: str
):

    task = TaskStore.get_task(task_id)

    if not task:
        return {
            "error": "Task not found"
        }

    return task["diffs"]