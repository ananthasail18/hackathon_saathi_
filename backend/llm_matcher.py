import json
from groq import Groq
from pydantic import BaseModel
from config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

class MatchResult(BaseModel):
    score: int
    reason: str
    action_recommendation: str

def evaluate_hackathon_match(user_profile: dict, hackathon_details: dict) -> MatchResult:
    """
    Uses Groq LLM to evaluate if a hackathon is a good fit for the user.
    """
    if not settings.GROQ_API_KEY:
        return MatchResult(
            score=0,
            reason="Groq API Key not configured. Please set GROQ_API_KEY in .env.",
            action_recommendation="Skip"
        )
        
    prompt = f"""
    You are an AI Hackathon Matchmaker Agent.
    
    User Profile:
    {json.dumps(user_profile, indent=2)}
    
    Hackathon Details:
    {json.dumps(hackathon_details, indent=2)}
    
    Evaluate how well the user's skills and interests match this hackathon.
    Provide your response as a valid JSON object with the following keys:
    - "score": An integer from 0 to 100 representing the match percentage.
    - "reason": A brief, compelling 2-sentence explanation of why it's a good (or bad) fit.
    - "action_recommendation": Either "Highly Recommended", "Recommended", or "Skip".
    
    Output strictly JSON, nothing else.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful JSON-outputting assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        result_json = json.loads(completion.choices[0].message.content)
        return MatchResult(
            score=result_json.get("score", 0),
            reason=result_json.get("reason", "Could not determine reason."),
            action_recommendation=result_json.get("action_recommendation", "Skip")
        )
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return MatchResult(
            score=0, 
            reason=f"Failed to analyze due to error: {str(e)}", 
            action_recommendation="Skip"
        )
