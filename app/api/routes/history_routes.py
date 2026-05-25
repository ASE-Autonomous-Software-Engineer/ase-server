from fastapi import APIRouter

from app.database.database import (
    SessionLocal
)

from app.database.models.task_model import (
    Task
)

router = APIRouter(
    prefix="/history",
    tags=["history"]
)

@router.get("/tasks")

async def get_tasks():

    db = SessionLocal()

    tasks = db.query(Task).all()

    return [
        {
            "id": task.id,
            "objective": task.objective,
            "status": task.status,
            "created_at": (
                task.created_at
            )
        }

        for task in tasks
    ]