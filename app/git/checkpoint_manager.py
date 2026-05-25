from git import Repo

class CheckpointManager:

    @staticmethod
    def create_checkpoint(repo_path, message):

        repo = Repo(repo_path)

        repo.git.add(A=True)

        repo.index.commit(message)

    @staticmethod
    def rollback(repo_path):

        repo = Repo(repo_path)

        repo.git.reset("--hard", "HEAD~1")