from app.git.checkpoint_manager import (
    CheckpointManager
)

class RecoveryEngine:

    @staticmethod
    def recover(repo_path):

        CheckpointManager.rollback(
            repo_path
        )