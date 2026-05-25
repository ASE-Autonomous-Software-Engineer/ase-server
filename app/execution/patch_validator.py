class PatchValidator:

    @staticmethod
    def validate(content: str):

        dangerous_keywords = [
            "rm -rf",
            "drop database",
            "delete *",
            "os.remove",
            "shutil.rmtree",
            "subprocess.Popen",
            "eval(",
            "exec("
        ]

        lowered = content.lower()

        for keyword in dangerous_keywords:

            if keyword.lower() in lowered:
                return False

        return True