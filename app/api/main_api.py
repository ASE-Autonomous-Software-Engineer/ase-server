

from fastapi import FastAPI

from app.api.routes.execution_routes import (
    router as execution_router
)

from app.api.routes.websocket_routes import (
    router as websocket_router
)

from app.api.routes.task_routes import (
    router as task_router
)

from app.api.routes.log_routes import (
    router as log_router
)

from app.api.routes.workflow_routes import (
    router as workflow_router
)

from app.api.routes.diff_routes import (
    router as diff_router
)

from app.api.routes.memory_routes import (
    router as memory_router
)

from app.api.routes.timeline_routes import (
    router as timeline_router
)

from app.api.routes.sandbox_routes import (
    router as sandbox_router
)

from app.api.routes.metrics_routes import (
    router as metrics_router
)
from app.api.routes.repository_routes import (
    router as repository_router
)
from app.database.database import (
    Base,
    engine
)

import app.database.models
from app.api.routes.history_routes import (
    router as history_router
)

from fastapi.middleware.cors import (
    CORSMiddleware
)


Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Autonomous Software Engineer",
    version="1.0.0"
)

# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(execution_router)

app.include_router(websocket_router)

app.include_router(task_router)

app.include_router(log_router)

app.include_router(workflow_router)

app.include_router(diff_router)

app.include_router(memory_router)

app.include_router(timeline_router)

app.include_router(sandbox_router)

app.include_router(metrics_router)
app.include_router(
    repository_router
)

app.include_router(
    history_router
)