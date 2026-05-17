from langgraph.graph import StateGraph # type: ignore

workflow = StateGraph(dict)

def clean_node(state):

    state["cleaned"] = True

    return state


def train_node(state):

    state["trained"] = True

    return state


workflow.add_node("clean", clean_node)
workflow.add_node("train", train_node)

workflow.set_entry_point("clean")

workflow.add_edge("clean", "train")

graph = workflow.compile()