from langgraph.graph import StateGraph, END

from app.runtime.state import AgentState
from app.agents.planner_agent import planner_node
from app.agents.repository_agent import repository_analysis_node
from app.agents.patch_generation_agent import (
    patch_generation_node
)
from app.agents.test_agent import test_execution_node
from app.agents.debugging_agent import debugging_node
from app.agents.file_selection_agent import (
    file_selection_node
)
from app.execution.patch_execution_node import (
    patch_execution_node
)
from app.execution.checkpoint_node import (
    checkpoint_node
)
from app.agents.coding_agent import (
    coding_node
)
from app.memory.context_retrieval_node import (
    context_retrieval_node
)
workflow = StateGraph(AgentState)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "repository_analysis",
    repository_analysis_node
)

workflow.add_node(
    "patch_generation",
    patch_generation_node
)

workflow.add_node(
    "testing",
    test_execution_node
)

workflow.add_node(
    "debugging",
    debugging_node
)
workflow.add_node(
    "file_selection",
    file_selection_node
)

workflow.add_node(
    "patch_execution",
    patch_execution_node
)
workflow.add_node(
    "checkpoint",
    checkpoint_node
)
workflow.add_node(
    "coding",
    coding_node
)
workflow.add_node(
    "context_retrieval",
    context_retrieval_node
)
# -----------------------------
# ENTRY POINT
# -----------------------------

workflow.set_entry_point("planner")

# -----------------------------
# EXECUTION FLOW
# -----------------------------

workflow.add_edge(
    "planner",
    "repository_analysis"
)

workflow.add_edge(
    "repository_analysis",
    "context_retrieval"
)

workflow.add_edge(
    "context_retrieval",
    "file_selection"
)
workflow.add_edge(
    "file_selection",
    "patch_generation"
)
workflow.add_edge(
    "patch_generation",
    "patch_execution"
)
workflow.add_edge(
    "patch_execution",
    "checkpoint"
)

workflow.add_edge(
    "checkpoint",
    "testing"
)

# -----------------------------
# CONDITIONAL RETRY LOGIC
# -----------------------------

def route_after_testing(state):

    if state.get("tests_failed"):

        if state["debug_attempts"] >= 3:
            return END

        return "debugging"

    return END

workflow.add_conditional_edges(
    "testing",
    route_after_testing
)

workflow.add_edge(
    "debugging",
    "coding"
)



# -----------------------------
# COMPILE GRAPH
# -----------------------------

graph = workflow.compile()