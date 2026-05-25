from fastapi import APIRouter

from pydantic import BaseModel

from app.git.repository_cloner import (
    RepositoryCloner
)

from app.memory.repository_indexer import (
    index_repository
)

router = APIRouter(
    prefix="/repository",
    tags=["repository"]
)

class CloneRequest(BaseModel):

    github_url: str

@router.post("/clone")

async def clone_repository(
    request: CloneRequest
):

    # -----------------------------
    # CLONE REPOSITORY
    # -----------------------------

    result = (
        RepositoryCloner
        .clone_repository(
            request.github_url
        )
    )

    # -----------------------------
    # INDEX REPOSITORY
    # -----------------------------

    index_repository(
        result["path"]
    )

    # -----------------------------
    # RETURN RESPONSE
    # -----------------------------

    return {
        "repo_id": result["repo_id"],
        "repository_path": result["path"],
        "status": "indexed"
    }