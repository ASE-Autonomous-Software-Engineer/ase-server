
import difflib

class DiffTracker:

    @staticmethod
    def generate_diff(
        before: str,
        after: str,
        file_path: str
    ):

        diff = difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"{file_path}_before",
            tofile=f"{file_path}_after",
            lineterm=""
        )

        return "\n".join(diff)