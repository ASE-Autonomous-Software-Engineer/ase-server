from langchain_community.chat_models import ChatOllama

coder_model = ChatOllama(
    model="qwen2.5-coder:14b",
    temperature=0
)

def coding_node(state):

    repository_summary = "\n".join(
        [f["file"] for f in state["repository_map"][:50]]
    )

    prompt = f"""
    You are an elite software engineer.

    OBJECTIVE:
    {state["objective"]}

    REPOSITORY:
    {repository_summary}

    TASK:
    1. Identify relevant files
    2. Generate implementation code
    3. Explain modifications
    """

    response = coder_model.invoke(prompt)

    state["generated_code"] = response.content

    return state