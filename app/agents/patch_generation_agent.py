from langchain_community.chat_models import ChatOllama

from app.runtime.event_bus import EventBus
from app.runtime.task_store import TaskStore
from app.observability.execution_logger import ExecutionLogger

patch_model = ChatOllama(
    model="qwen2.5-coder:14b",
    temperature=0
)

async def patch_generation_node(state):

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "patch_generation",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "patch_generation",
        "running"
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Generating autonomous patch..."
    )

    target_files = "\n".join(
        state["target_files"]
    )

    retrieved_context = "\n\n".join([

        f"""
FILE: {ctx['file']}

CODE:
{ctx['content']}
"""

        for ctx in state["memory_context"]
    ])

    prompt = f"""
You are an elite autonomous software engineer.

OBJECTIVE:
{state["objective"]}

TARGET FILES:
{target_files}

RELEVANT REPOSITORY CONTEXT:
{retrieved_context}
"""

    response = patch_model.invoke(prompt)

    state["generated_code"] = response.content

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "patch_generation",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "patch_generation",
        "completed"
    )

    return state