import spacy
from textblob import TextBlob
from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum
from typing import List
import backend



# --- API Metadata ---
app = FastAPI(
    title="NLP-Powered Risk Assessment Service",
    description="An advanced API that uses Natural Language Processing to determine task importance.",
    version="3.1.0", # Version bump!
)

# Load the pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# --- NEW: Define words that signal immediate urgency ---
URGENCY_TRIGGERS = ["now", "today", "tonight", "eod", "asap", "minute", "hour"]

# --- Enums and Models ---
class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical 🌶️"

class Task(BaseModel):
    title: str = Field(..., example="Deploy critical security patch by Friday EOD")
    description: str = Field(..., example="A major vulnerability was found in the authentication service. Failure to patch could result in a data breach affecting over $50k in assets.")

class RiskResponse(BaseModel):
    risk_score: int = Field(..., example=95)
    risk_level: RiskLevel = Field(..., example=RiskLevel.CRITICAL)
    factors: List[str] = Field(..., example=["Detected deadline: 'by Friday EOD'", "Detected monetary value: '$50k'", "High-urgency sentiment detected"])

@app.post("/calculate", response_model=RiskResponse)
async def calculate_risk(task: Task):
    """
    Analyzes a task using NLP to determine its risk score and level.
    """
    score = 0
    factors = []
    
    # --- NLP Analysis ---
    title_doc = nlp(task.title)
    desc_doc = nlp(task.description)
    
    if title_doc and title_doc[0].pos_ == "VERB":
        score += 25
        factors.append(f"Action-oriented title starting with '{title_doc[0].text}'")

    sentiment = TextBlob(task.description).sentiment
    if sentiment.polarity < -0.3:
        score += 30
        factors.append(f"High-urgency sentiment detected (Polarity: {sentiment.polarity:.2f})")

    combined_doc = nlp(task.title + ". " + task.description)
    for ent in combined_doc.ents:
        # --- MODIFIED: Smarter Deadline Scoring ---
        if ent.label_ in ["DATE", "TIME"]:
            score += 20 # Base score for any deadline
            factors.append(f"Detected deadline: '{ent.text}'")
            # Check for urgency keywords within the deadline text
            if any(trigger in ent.text.lower() for trigger in URGENCY_TRIGGERS):
                score += 40 # Add a large urgency bonus!
                factors.append("Deadline is highly urgent!")

        if ent.label_ == "MONEY":
            score += 35
            factors.append(f"Detected monetary value: '{ent.text}'")
        if ent.label_ == "ORG":
             score += 10
             factors.append(f"Mention of organization: '{ent.text}'")

    # --- Final Score Calculation ---
    risk_score = max(0, min(100, score))

    if risk_score >= 80:
        level = RiskLevel.CRITICAL
    elif risk_score >= 60:
        level = RiskLevel.HIGH
    elif risk_score >= 30:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
        if not factors:
            factors.append("NLP analysis found no significant risk factors.")

    return RiskResponse(
        risk_score=risk_score,
        risk_level=level,
        factors=factors
    )