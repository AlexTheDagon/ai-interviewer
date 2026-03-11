import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import InterviewState

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

def generate_question(state: InterviewState) -> dict:
    """Generates the next interview question based on the topic and transcript."""
    system_prompt = (
        f"You are a professional interviewer conducting a focused interview on: '{state['topic']}'. "
        "Your goal is to ask engaging, sequential questions."
    )
    
    history = ""
    if state['transcript']:
        history = "Previous Questions and Answers:\n"
        for qa in state['transcript']:
            history += f"Q: {qa['q']}\nA: {qa['a']}\n\n"
            
    user_prompt = (
        f"{history}Based on the conversation above, generate the next logical, thought-provoking question. "
        "If this is the first question, ask a broad introductory question about the topic. "
        "Provide ONLY the question text. Keep it concise."
    )
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
    return {"current_question": response.content.strip()}

def summarize_interview(state: InterviewState) -> dict:
    """Generates a summary, extracts keywords, and scores sentiment."""
    transcript_text = "\n".join([f"Q: {qa['q']}\nA: {qa['a']}" for qa in state['transcript']])
    
    prompt = f"""
    Analyze the following interview transcript about '{state['topic']}'.
    Return the analysis strictly as a JSON object with the following keys:
    - "themes": A list of 2-3 key themes discussed.
    - "key_points": A short paragraph summarizing the user's main arguments.
    - "sentiment_label": A string (Positive, Neutral, or Negative).
    - "sentiment_score": An integer from 1 to 10 evaluating the positivity/enthusiasm.
    - "keywords": A list of 5 important keywords.

    Transcript:
    {transcript_text}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    raw_content = response.content.strip()
    if raw_content.startswith("```json"):
        raw_content = raw_content[7:-3].strip()
    elif raw_content.startswith("```"):
        raw_content = raw_content[3:-3].strip()
        
    try:
        summary_data = json.loads(raw_content)
    except json.JSONDecodeError:
        summary_data = {"error": "Failed to parse JSON", "raw": raw_content}
        
    return {"summary": summary_data}

def save_data(state: InterviewState) -> dict:
    """Stores the transcript and summary to a JSON file inside an 'interviews' folder."""
    output_data = {
        "topic": state["topic"],
        "transcript": state["transcript"],
        "analysis": state["summary"]
    }
    
    safe_topic = "".join(c if c.isalnum() else "_" for c in state['topic']).lower()
    filename = f"interview_{safe_topic}.json"
    
    # Ensure the 'interviews' directory exists
    save_dir = "interviews"
    os.makedirs(save_dir, exist_ok=True)
    
    # Create the full file path
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(output_data, f, indent=4)
        
    return state