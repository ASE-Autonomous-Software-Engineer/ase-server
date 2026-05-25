from app.memory.vector_store import (
    MemoryStore
)

from app.runtime.task_store import (
    TaskStore
)

from app.runtime.event_bus import (
    EventBus
)

from app.observability.execution_logger import (
    ExecutionLogger
)

async def context_retrieval_node(state):

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "context_retrieval",
        "status": "running"
    })

    await ExecutionLogger.log(
        state["task_id"],
        "Retrieving repository memory context..."
    )

    results = MemoryStore.retrieve_memory(
        state["objective"]
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    contexts = []

    for doc, meta in zip(
        documents,
        metadatas
    ):

        contexts.append({
            "content": doc,
            "file": meta.get("file")
        })

    state["memory_context"] = contexts

    TaskStore.set_memory(
        state["task_id"],
        contexts
    )

    await EventBus.emit({
        "task_id": state["task_id"],
        "node": "context_retrieval",
        "status": "completed"
    })

    return state