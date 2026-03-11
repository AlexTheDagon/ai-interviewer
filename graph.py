from langgraph.graph import StateGraph, END
from state import InterviewState
from nodes import generate_question, summarize_interview, save_data

workflow = StateGraph(InterviewState)

workflow.add_node("generate_question", generate_question)
workflow.add_node("summarize_interview", summarize_interview)
workflow.add_node("save_data", save_data)

# Dynamic routing based on transcript length
def route_entry(state: InterviewState):
    if len(state["transcript"]) < state["max_questions"]:
        return "generate_question"
    else:
        return "summarize_interview"

workflow.set_conditional_entry_point(route_entry)
workflow.add_edge("generate_question", END)
workflow.add_edge("summarize_interview", "save_data")
workflow.add_edge("save_data", END)

app = workflow.compile()