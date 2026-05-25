import uuid
import shutil

from pathlib import Path
from git import Repo

class RepositoryCloner:

    BASE_DIR = "repositories"

    @staticmethod
    def clone_repository(repo_url: str):

        repo_id = str(uuid.uuid4())

        clone_path = (
            Path(
                RepositoryCloner.BASE_DIR
            ) / repo_id
        )

        if clone_path.exists():

            shutil.rmtree(clone_path)

        Repo.clone_from(
            repo_url,
            clone_path
        )

        return {
            "repo_id": repo_id,
            "path": str(clone_path)
        }