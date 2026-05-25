from langchain_community.chat_models import ChatOllama
from app.runtime.event_bus import EventBus
from app.runtime.task_store import TaskStore
from app.observability.execution_logger import ExecutionLogger
planner_model = ChatOllama(
    model="deepseek-r1:14b",
    temperature=0
)

async def planner_node(state):

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "planner",
        "status": "running"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "planner",
        "running"
    )

    TaskStore.add_timeline_event(
        state["task_id"],
        {
            "node": "planner",
            "status": "running"
        }
    )

    await ExecutionLogger.log(
        state["task_id"],
        "Planning execution strategy..."
    )
    prompt = f"""
    You are an elite software architect.

    OBJECTIVE:
    {state["objective"]}

    Create:
    1. execution strategy
    2. implementation steps
    3. testing strategy
    4. rollback risks
    """

    response = planner_model.invoke(prompt)

    state["execution_plan"] = [
        response.content
    ]

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "planner",
        "status": "completed"
    })

    TaskStore.update_workflow(
        state["task_id"],
        "planner",
        "completed"
    )

    return state