from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str

@app.post("/calculate")
def calculate_risk(task: Task):
    """Calculates a risk score based on the length of the task's content."""
    score = len(task.title) + len(task.description)
    # Clamp the score between 0 and 100
    risk_score = max(0, min(100, score))
    return {"risk_score": risk_score}