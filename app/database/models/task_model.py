from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database.database import (
    Base
)

class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        String,
        primary_key=True,
        index=True
    )

    objective = Column(Text)

    status = Column(String)

    repository_path = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )