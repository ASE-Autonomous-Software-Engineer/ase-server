import subprocess

from app.events.event_emitter import (
    EventEmitter
)

SAFE_COMMANDS = [
    "pytest",
    "python",
    "pip",
    "npm test",
    "npm run test",
    "uvicorn",
    "flake8",
    "black",
    "isort"
]

class TerminalExecutor:

    @staticmethod
    def execute(command: str):

        # --------------------------------
        # SAFETY VALIDATION
        # --------------------------------

        is_safe = any(
            command.startswith(cmd)
            for cmd in SAFE_COMMANDS
        )

        if not is_safe:

            return {
                "status": "blocked",
                "error": "Unsafe command detected"
            }

        # --------------------------------
        # EMIT START EVENT
        # --------------------------------

        EventEmitter.emit(
            "terminal_execution_started",
            {
                "command": command
            }
        )

        try:

            # --------------------------------
            # EXECUTE COMMAND
            # --------------------------------

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            output = {
                "status": "completed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

            # --------------------------------
            # EMIT COMPLETION EVENT
            # --------------------------------

            EventEmitter.emit(
                "terminal_execution_completed",
                output
            )

            return output

        except subprocess.TimeoutExpired:

            timeout_output = {
                "status": "timeout",
                "error": "Command execution timed out"
            }

            EventEmitter.emit(
                "terminal_execution_failed",
                timeout_output
            )

            return timeout_output

        except Exception as e:

            error_output = {
                "status": "failed",
                "error": str(e)
            }

            EventEmitter.emit(
                "terminal_execution_failed",
                error_output
            )

            return error_output