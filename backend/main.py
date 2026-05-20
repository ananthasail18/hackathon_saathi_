from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auto_apply_agent import auto_fill_form
from calendar_agent import add_hackathon_to_calendar
import asyncio

app = FastAPI(title="Hackathon Saathi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfile(BaseModel):
    name: str
    skills: list[str]
    interests: list[str]
    bio: str

class ApplyRequest(BaseModel):
    profile: dict
    url: str

class CalendarRequest(BaseModel):
    title: str
    start_date: str
    end_date: str
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Hackathon Saathi API"}

def run_agent_in_background(profile: dict, url: str):
    # Create a new event loop for the background thread to run Playwright
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(auto_fill_form(profile, url))
    loop.close()

@app.post("/api/apply")
def trigger_apply_agent(req: ApplyRequest, background_tasks: BackgroundTasks):
    """Launches the Playwright agent in the background so the UI doesn't hang."""
    background_tasks.add_task(run_agent_in_background, req.profile, req.url)
    return {"status": "Agent Launched. Please check the new browser window."}

@app.post("/api/calendar/sync")
def sync_to_calendar(req: CalendarRequest):
    """Syncs the hackathon to Google Calendar."""
    success = add_hackathon_to_calendar(req.title, req.start_date, req.end_date, req.url)
    if success:
        return {"status": "Success", "message": "Added to Google Calendar!"}
    return {"status": "Error", "message": "Failed to add to calendar. Check credentials."}
