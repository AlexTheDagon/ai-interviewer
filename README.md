# 🎙️ AI Interviewer (LangGraph & Gradio)

This project is a mini "AI Interviewer" application inspired by the Anthropic Interviewer tool. It conducts interactive, multi-turn interviews on user-selected topics, dynamically generates contextual questions, and provides a comprehensive summary of the user's responses.

## 🚀 Features
* **Dynamic Multi-Turn Conversations:** Uses **LangGraph** to manage the state and routing of the interview.
* **Contextual Questioning:** Leverages Google's **Gemini 2.5 Flash** model to generate 3-5 sequential questions based on the topic and previous answers.
* **Web UI:** Built with **Gradio** for a clean, accessible, and responsive user experience.
* **Bonus - Advanced Analysis:** Automatically extracts themes, key points, sentiment scores, and keywords from the interview transcript.
* **Local Storage:** Saves the complete transcript and analytical summary locally as a JSON file in a generated `/interviews` directory.

## 🏗️ Architecture & Structure
To maintain code clarity and scalability, the application logic is separated into distinct modules:
* `state.py`: Defines the `TypedDict` state schema that flows through the LangGraph application.
* `nodes.py`: Contains the worker functions (nodes) that interact with the LLM to generate questions, summarize interviews, and save data. 
* `graph.py`: Handles the routing logic, conditional edges, and compiles the LangGraph state machine.
* `app_ui.py`: The entry point that builds the Gradio interface and connects user inputs to the graph.

## 🛠️ Setup Instructions

**1. Clone the repository and navigate to the project directory:**
```bash
git clone https://github.com/AlexTheDagon/ai-interviewer
cd ai-interviewer```

**2. Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt```

**4. Add your API Key:**
```bash
GOOGLE_API_KEY="your_actual_api_key_here"```

**5. Run the application:**
```bash
python app_ui.py```