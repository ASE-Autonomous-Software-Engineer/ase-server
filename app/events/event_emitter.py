import structlog
from datetime import datetime

logger = structlog.get_logger()

class EventEmitter:

    @staticmethod
    def emit(event_type: str, payload: dict):

        logger.info(
            "agent_event",
            timestamp=str(datetime.utcnow()),
            event_type=event_type,
            payload=payload
        )