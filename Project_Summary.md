# Hackathon Saathi - Project Summary

## 1. The Core Architecture
We established a modern, decoupled architecture:
*   **Frontend**: A React/TypeScript web application powered by Vite.
*   **Backend API**: A highly asynchronous Python backend powered by FastAPI.
*   **AI Engine**: Integrated with Groq's API, utilizing the blazing-fast `llama-3.1-8b-instant` model to act as the core brain of the system.

## 2. The Premium UI/UX Dashboard
We built a beautiful, high-end dashboard without relying on bulky CSS frameworks. 
*   **Aesthetics**: Implemented a modern "Glassmorphism" design with a dark mode theme, subtle gradients, and micro-animations to give it a premium feel.
*   **Features**: It includes a "Discover Matches" tab to view hackathons and an "Agent Configuration Profile" tab to store the user's resume, bio, and skills.

## 3. Agent 1: The AI Matchmaker
Instead of blindly showing all hackathons, the system acts as a personal curator.
*   **How it works**: We built `llm_matcher.py`, which takes unstructured hackathon data and compares it against the user's profile.
*   **Output**: The LLM assigns a Match Score (0-100%) and generates a personalized, 2-sentence explanation of exactly why a hackathon fits the user's specific skill set.

## 4. Agent 2: The Discovery Scraper
To ensure the platform is always up to date, we built an ingestion engine.
*   **How it works**: We wrote `scraper.py`, a Playwright-based autonomous web crawler.
*   **Capability**: It navigates to platforms like Devfolio, parses the DOM, extracts the latest active hackathons, and feeds them back into the system for matching.

## 5. Agent 3: The Human-in-the-Loop Auto-Apply Agent
This is the flagship feature to eliminate the redundancy of form-filling.
*   **How it works**: When you click "Agent Auto-Apply" on the frontend, it triggers `auto_apply_agent.py`.
*   **Execution**: It launches a visible browser instance, navigates to the application page (e.g., Devpost), and uses the Groq LLM to intelligently map your profile data to the specific form fields it finds on the page.
*   **Safety First**: Following your excellent suggestion, the agent types out all the answers but **intentionally stops** without submitting, leaving the browser open for you to review the fields and manually hit "Submit."

## 6. Agent 4: Google Calendar Sync
To keep you organized, we integrated calendar tracking.
*   **How it works**: We built `calendar_agent.py` to interface with the Google Calendar API via OAuth2.
*   **Demo Optimization**: Once you apply for a hackathon, clicking the sync button instantly opens Google Calendar in a new tab while the backend seamlessly updates the UI state (mocking the API success for a flawless presentation demo). 

## 7. Submission Artifacts
Finally, we automated the capture of your project by writing a script (`take_screenshots.py`) that autonomously navigated through your dashboard and saved high-quality screenshots of the workflow directly to your project folder for your final presentation.
