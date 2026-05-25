import uuid

from fastapi import (
    APIRouter,
    BackgroundTasks
)

from app.graph.workflow import graph

from app.api.schemas.execution_schema import (
    ExecuteTaskRequest
)

from app.runtime.task_store import (
    TaskStore
)

from app.database.database import (
    SessionLocal
)

from app.database.models.task_model import (
    Task
)

router = APIRouter()

# --------------------------------
# BACKGROUND EXECUTION
# --------------------------------

async def run_workflow(state):

    await graph.ainvoke(state)

# --------------------------------
# EXECUTION ROUTE
# --------------------------------

@router.post("/execute")

async def execute_task(
    request: ExecuteTaskRequest,
    background_tasks: BackgroundTasks
):

    task_id = str(uuid.uuid4())

    # --------------------------------
    # CREATE IN-MEMORY TASK
    # --------------------------------

    TaskStore.create_task(
        task_id,
        request.objective
    )

    # --------------------------------
    # SAVE TO DATABASE
    # --------------------------------

    db = SessionLocal()

    task = Task(
        id=task_id,
        objective=request.objective,
        status="running",
        repository_path=request.repository_path
    )

    db.add(task)

    db.commit()

    db.close()

    # --------------------------------
    # INITIAL STATE
    # --------------------------------

    initial_state = {

        "task_id": task_id,

        "objective": request.objective,

        "repository_path": (
            request.repository_path
        ),

        "current_step": "",

        "execution_plan": [],

        "completed_steps": [],

        "failed_steps": [],

        "available_tools": [],

        "tool_results": {},

        "execution_logs": [],

        "generated_code": None,

        "test_results": None,

        "retry_count": 0,

        "requires_human_approval": False,

        "memory_context": [],

        "final_output": None,

        "repository_map": [],

        "target_files": [],

        "debug_attempts": 0,

        "tests_failed": False,

        "debug_analysis": None,

        "supervisor_plan": None,

        "approval_status": None,

        "awaiting_approval": False
    }

    # --------------------------------
    # RUN WORKFLOW
    # --------------------------------

    background_tasks.add_task(
        run_workflow,
        initial_state
    )

    return {
        "task_id": task_id,
        "status": "started"
    }