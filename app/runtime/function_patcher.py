from pathlib import Path

class FunctionPatcher:

    @staticmethod
    def replace_function(
        file_path,
        start_line,
        end_line,
        new_function
    ):

        path = Path(file_path)

        lines = path.read_text().splitlines()

        updated_lines = (
            lines[:start_line - 1]
            +
            new_function.splitlines()
            +
            lines[end_line:]
        )

        path.write_text(
            "\n".join(updated_lines)
        )