from pathlib import Path

from app.memory.vector_store import (
    MemoryStore
)

from app.memory.code_chunker import (
    CodeChunker
)

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    "dist",
    "build"
}

def index_repository(repo_path: str):

    for path in Path(repo_path).rglob("*"):

        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRS
        ):
            continue

        if path.is_file():

            try:

                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                chunks = (
                    CodeChunker
                    .chunk_content(content)
                )

                for idx, chunk in enumerate(chunks):

                    MemoryStore.save_memory(
                        memory_id=f"{path}_{idx}",
                        content=chunk,
                        metadata={
                            "file": str(path),
                            "chunk": idx
                        }
                    )

            except Exception as e:

                print(
                    f"Indexing failed: {path} -> {e}"
                )