from langchain_community.chat_models import ChatOllama

from app.runtime.event_bus import EventBus
from app.runtime.task_store import TaskStore
from app.observability.execution_logger import ExecutionLogger

debugger_model = ChatOllama(
    model="deepseek-r1:14b",
    temperature=0
)

async def debugging_node(state):

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "debugging",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "debugging",
        "running"
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Analyzing failed tests..."
    )

    prompt = f"""
    You are an elite debugging engineer.

    OBJECTIVE:
    {state["objective"]}

    GENERATED CODE:
    {state["generated_code"]}

    TEST FAILURES:
    {state["test_results"]}
    """

    response = debugger_model.invoke(prompt)

    state["debug_analysis"] = response.content

    state["debug_attempts"] += 1

    await ExecutionLogger.log(
        state["task_id"],
        f"Debug attempt #{state['debug_attempts']}"
    )

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "debugging",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "debugging",
        "completed"
    )

    return state