from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database.database import (
    Base
)

class ExecutionLog(Base):

    __tablename__ = "execution_logs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    task_id = Column(String)

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )