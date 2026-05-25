from pathlib import Path

from app.intelligence.ast_parser import (
    ASTParser
)

class SymbolExtractor:

    @staticmethod
    def extract(path):

        content = Path(path).read_text(
            encoding="utf-8",
            errors="ignore"
        )

        tree = ASTParser.parse_file(
            content
        )

        return {
            "functions": (
                ASTParser.extract_functions(tree)
            ),
            "classes": (
                ASTParser.extract_classes(tree)
            )
        }