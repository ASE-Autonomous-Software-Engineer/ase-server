from langchain_community.chat_models import ChatOllama

supervisor_model = ChatOllama(
    model="deepseek-r1:14b",
    temperature=0
)

def supervisor_node(state):

    prompt = f"""
    You are an autonomous engineering supervisor.

    OBJECTIVE:
    {state["objective"]}

    Decide:
    1. which agents should execute
    2. execution ordering
    3. risk assessment
    4. delegation strategy
    """

    response = supervisor_model.invoke(prompt)

    state["supervisor_plan"] = response.content

    return state