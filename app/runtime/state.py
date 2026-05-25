from typing import TypedDict, List, Dict, Optional, Any

class AgentState(TypedDict):

    # --------------------------------
    # TASK METADATA
    # --------------------------------

    task_id: str

    objective: str

    repository_path: str

    current_step: str

    # --------------------------------
    # EXECUTION PLANNING
    # --------------------------------

    execution_plan: List[str]

    supervisor_plan: Optional[str]

    # --------------------------------
    # REPOSITORY ANALYSIS
    # --------------------------------

    repository_map: List[Dict]

    target_files: List[str]

    # --------------------------------
    # MEMORY
    # --------------------------------

    memory_context: List[Dict]

    # --------------------------------
    # CODE GENERATION
    # --------------------------------

    generated_code: Optional[str]

    debug_analysis: Optional[str]

    # --------------------------------
    # EXECUTION RESULTS
    # --------------------------------

    test_results: Optional[str]

    tests_failed: bool

    final_output: Optional[str]

    # --------------------------------
    # OBSERVABILITY
    # --------------------------------

    execution_logs: List[str]

    tool_results: Dict[str, Any]

    completed_steps: List[str]

    failed_steps: List[str]

    # --------------------------------
    # RETRY + DEBUGGING
    # --------------------------------

    retry_count: int

    debug_attempts: int

    # --------------------------------
    # HUMAN CONTROL
    # --------------------------------

    requires_human_approval: bool

    # --------------------------------
    # TOOLS
    # --------------------------------

    available_tools: List[str]