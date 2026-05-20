from llm_matcher import evaluate_hackathon_match
from config import settings

if __name__ == "__main__":
    print(f"Using Groq API Key: {'Set' if settings.GROQ_API_KEY else 'Not Set'}")
    
    mock_profile = {
        "name": "Anant",
        "skills": ["Python", "FastAPI", "React", "AI Agents"],
        "interests": ["Generative AI", "Web3", "Automation"],
        "bio": "I love building autonomous agents and AI-driven products."
    }
    
    mock_hackathon = {
        "title": "Agentic AI Hackathon 2026",
        "platform": "Devpost",
        "description": "Build the next generation of AI agents using LangChain and LLMs.",
        "tags": ["AI", "Agents", "Python"]
    }
    
    print("\nEvaluating Match...")
    result = evaluate_hackathon_match(mock_profile, mock_hackathon)
    print(f"Score: {result.score}/100")
    print(f"Recommendation: {result.action_recommendation}")
    print(f"Reason: {result.reason}")
