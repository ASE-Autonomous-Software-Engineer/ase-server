class ImportManager:

    @staticmethod
    def add_import(
        content,
        import_line
    ):

        if import_line in content:
            return content

        return import_line + "\n" + content