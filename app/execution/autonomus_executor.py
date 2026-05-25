from app.execution.patch_validator import (
    PatchValidator
)

from app.execution.patch_applier import (
    PatchApplier
)

from app.execution.diff_tracker import (
    DiffTracker
)

from app.runtime.task_store import (
    TaskStore
)

class AutonomousExecutor:

    @staticmethod
    def execute_patch(
        task_id,
        file_path,
        updated_content
    ):

        valid = PatchValidator.validate(
            updated_content
        )

        if not valid:

            return {
                "status": "rejected"
            }

        result = PatchApplier.apply_patch(
            file_path,
            updated_content
        )

        # --------------------------------
        # TRACK DIFF
        # --------------------------------

        diff = DiffTracker.generate_diff(
            result["before_content"],
            updated_content,
            file_path
        )

        TaskStore.add_diff(
            task_id,
            {
                "file": file_path,
                "diff": diff
            }
        )

        return result