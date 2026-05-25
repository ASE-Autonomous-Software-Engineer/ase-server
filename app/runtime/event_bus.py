

from app.api.websocket.websocket_manager import (
    manager
)

class EventBus:

    @staticmethod
    async def emit(event):

        await manager.broadcast(event)