from langchain_community.chat_models import ChatOllama

from app.runtime.event_bus import EventBus
from app.runtime.task_store import TaskStore
from app.observability.execution_logger import ExecutionLogger

selector_model = ChatOllama(
    model="deepseek-r1:14b",
    temperature=0
)

async def file_selection_node(state):

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "file_selection",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "file_selection",
        "running"
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Selecting target files..."
    )

    repository_files = "\n".join([
        file["file"]
        for file in state["repository_map"][:200]
    ])

    prompt = f"""
    You are an expert software architect.

    OBJECTIVE:
    {state["objective"]}

    REPOSITORY FILES:
    {repository_files}

    Return ONLY the most relevant files
    that should be modified.
    """

    response = selector_model.invoke(prompt)

    selected_files = [
        file.strip()
        for file in response.content.split("\n")
        if file.strip()
    ]

    state["target_files"] = selected_files

    await ExecutionLogger.log(
        state["task_id"],
        f"Selected {len(selected_files)} files"
    )

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "file_selection",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "file_selection",
        "completed"
    )

    return state