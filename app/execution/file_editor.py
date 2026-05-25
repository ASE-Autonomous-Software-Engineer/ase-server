from pathlib import Path
from app.events.event_emitter import EventEmitter

class FileEditor:

    @staticmethod
    def write_file(path: str, content: str):

        EventEmitter.emit(
            "file_write_started",
            {"path": path}
        )

        Path(path).write_text(content)

        EventEmitter.emit(
            "file_write_completed",
            {"path": path}
        )