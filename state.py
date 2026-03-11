from typing import TypedDict, List, Dict, Any

class InterviewState(TypedDict):
    topic: str
    max_questions: int
    current_question: str
    transcript: List[Dict[str, str]]
    summary: Dict[str, Any]