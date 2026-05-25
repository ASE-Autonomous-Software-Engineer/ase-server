import ast

class ASTParser:

    @staticmethod
    def parse_file(content: str):

        return ast.parse(content)

    @staticmethod
    def extract_functions(tree):

        functions = []

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno
                })

        return functions

    @staticmethod
    def extract_classes(tree):

        classes = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno
                })

        return classes