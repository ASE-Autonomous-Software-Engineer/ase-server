

from typing import Dict

class TaskStore:

    tasks: Dict = {}

    @classmethod
    def create_task(
        cls,
        task_id,
        initial_state
    ):

        cls.tasks[task_id] = {
            "state": initial_state,
            "logs": [],
            "workflow": {},
            "timeline": [],
            "diffs": [],
            "memory": []
        }

    @classmethod
    def update_state(
        cls,
        task_id,
        state
    ):

        cls.tasks[task_id]["state"] = state

    @classmethod
    def get_task(
        cls,
        task_id
    ):

        return cls.tasks.get(task_id)

    @classmethod
    def add_log(
        cls,
        task_id,
        log
    ):

        cls.tasks[task_id]["logs"].append(log)

    @classmethod
    def update_workflow(
        cls,
        task_id,
        node,
        status
    ):

        cls.tasks[task_id]["workflow"][node] = status

    @classmethod
    def add_timeline_event(
        cls,
        task_id,
        event
    ):

        cls.tasks[task_id]["timeline"].append(event)

    @classmethod
    def add_diff(
        cls,
        task_id,
        diff
    ):

        cls.tasks[task_id]["diffs"].append(diff)

    @classmethod
    def set_memory(
        cls,
        task_id,
        memory
    ):

        cls.tasks[task_id]["memory"] = memory