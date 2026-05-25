class ModelRouter:

    @staticmethod
    def route(task_type: str):

        if task_type == "planning":
            return "deepseek-r1:14b"

        if task_type == "coding":
            return "qwen2.5-coder:14b"

        if task_type == "debugging":
            return "deepseek-r1:14b"

        return "qwen2.5-coder:14b"