import gradio as gr
from graph import app
from state import InterviewState

def start_interview(topic):
    """Initializes the state and gets the first question."""
    if not topic.strip():
        return gr.update(value=""), [], None, "Please enter a topic."
    
    # Create fresh state
    state: InterviewState = {
        "topic": topic,
        "max_questions": 5, # Generating 3-5 questions as required
        "current_question": "",
        "transcript": [],
        "summary": {}
    }
    
    # Run graph to get the first question
    new_state = app.invoke(state)
    
    chat_history = [(None, new_state["current_question"])]
    return gr.update(interactive=False), chat_history, new_state, f"**Status:** Interview started on: '{topic}'"

def process_chat(user_message, chat_history, state):
    """Handles user answers, updates state, and routes the graph."""
    if state is None:
        return "", chat_history, state, "**Status:** Please start an interview first."
        
    # 1. Update state with the user's answer
    new_entry = {"q": state["current_question"], "a": user_message}
    state["transcript"].append(new_entry)
    chat_history.append((user_message, None))
    
    # 2. Invoke graph with updated state
    new_state = app.invoke(state)
    
    # 3. Handle Output
    if len(new_state["transcript"]) < new_state["max_questions"]:
        # We got a new question back
        chat_history.append((None, new_state["current_question"]))
        status = "**Status:** Interview in progress..."
    else:
        # Interview is over, we got a summary back
        summary = new_state["summary"]
        final_message = (
            f"**Interview Complete!**\n\n"
            f"**Themes:** {', '.join(summary.get('themes', []))}\n"
            f"**Key Points:** {summary.get('key_points', '')}\n"
            f"**Sentiment:** {summary.get('sentiment_label', 'N/A')} ({summary.get('sentiment_score', '')}/10)\n"
            f"**Keywords:** {', '.join(summary.get('keywords', []))}\n\n"
            f"*(Data successfully saved to the 'interviews' folder)*"
        )
        chat_history.append((None, final_message))
        status = "**Status:** Interview finished and saved."
        
    return "", chat_history, new_state, status

# --- Gradio UI Layout ---
with gr.Blocks(theme=gr.themes.Soft()) as ui:
    gr.Markdown("# 🎙️ AI Interviewer")
    gr.Markdown("A LangGraph-powered AI that conducts topical interviews and analyzes your responses.")
    
    # State storage
    app_state = gr.State(None)
    
    # Top Section: Topic Input and Button
    with gr.Row():
        topic_input = gr.Textbox(label="Interview Topic", placeholder="e.g., Remote work productivity", scale=4)
        start_btn = gr.Button("Start Interview", variant="primary", scale=1)
        
    status_text = gr.Markdown("**Status:** Enter a topic to begin.")
    
    # Bottom Section: Full-width Chat
    chatbot = gr.Chatbot(label="Interview Chat", height=500)
    msg_input = gr.Textbox(label="Your Answer", placeholder="Type your answer and hit Enter...")
            
    # Event wiring
    start_btn.click(
        start_interview, 
        inputs=[topic_input], 
        outputs=[topic_input, chatbot, app_state, status_text]
    )
    
    msg_input.submit(
        process_chat,
        inputs=[msg_input, chatbot, app_state],
        outputs=[msg_input, chatbot, app_state, status_text]
    )

if __name__ == "__main__":
    ui.launch(share=True)