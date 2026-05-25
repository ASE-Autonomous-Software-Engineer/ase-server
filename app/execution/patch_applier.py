from pathlib import Path

class PatchApplier:

    @staticmethod
    def apply_patch(
        file_path: str,
        updated_content: str
    ):

        path = Path(file_path)

        if not path.exists():

            return {
                "status": "file_not_found"
            }

        # --------------------------------
        # READ ORIGINAL
        # --------------------------------

        original_content = path.read_text()

        # --------------------------------
        # BACKUP
        # --------------------------------

        backup_path = path.with_suffix(
            path.suffix + ".bak"
        )

        backup_path.write_text(
            original_content
        )

        # --------------------------------
        # APPLY PATCH
        # --------------------------------

        path.write_text(updated_content)

        return {
            "status": "success",
            "backup": str(backup_path),
            "before_content": original_content
        }