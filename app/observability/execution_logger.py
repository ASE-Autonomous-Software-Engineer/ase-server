from datetime import datetime

from app.runtime.task_store import (
    TaskStore
)

from app.runtime.event_bus import (
    EventBus
)

from app.database.database import (
    SessionLocal
)

from app.database.models.log_model import (
    ExecutionLog
)

class ExecutionLogger:

    @staticmethod
    async def log(
        task_id,
        message,
        level="INFO"
    ):

        log = {
            "timestamp": (
                datetime.utcnow().isoformat()
            ),
            "level": level,
            "message": message
        }

        # --------------------------------
        # SAVE IN MEMORY
        # --------------------------------

        TaskStore.add_log(
            task_id,
            log
        )

        # --------------------------------
        # SAVE TO DATABASE
        # --------------------------------

        db = SessionLocal()

        db_log = ExecutionLog(
            task_id=task_id,
            message=message
        )

        db.add(db_log)

        db.commit()

        db.close()

        # --------------------------------
        # REALTIME WEBSOCKET EVENT
        # --------------------------------

        await EventBus.emit({
            "type": "log",
            "task_id": task_id,
            "data": log
        })