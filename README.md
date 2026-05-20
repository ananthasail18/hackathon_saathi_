# Hackathon Saathi 🚀

Your personal agentic hackathon companion. Discover perfect hackathons, automate the tedious application process using AI, and keep your schedule synced seamlessly.

## 🌟 Features

- **AI Matchmaker**: Uses Groq's LLM (`llama-3.1-8b-instant`) to semantically match your technical profile against live hackathon requirements.
- **Discovery Agent**: A Playwright-powered autonomous scraper that crawls platforms like Devfolio to find new opportunities.
- **Auto-Apply Agent (Human-in-the-loop)**: Automatically maps your resume/profile to complex application forms and fills them out for you. It pauses before submitting so you can review and approve!
- **Google Calendar Sync**: Integrates directly with the Google Calendar API to automatically schedule your hackathon dates.
- **Premium Dashboard**: A stunning, modern Glassmorphism UI built with React and Vite.

## 🏗️ Architecture

- **Frontend**: React, TypeScript, Vite, Vanilla CSS (Custom Design System)
- **Backend**: Python, FastAPI
- **AI/Agents**: Groq API, LangChain concepts, Playwright (Browser Automation)

---

## 🚀 Getting Started

Follow these steps to run the application locally on your machine.

### Prerequisites

- Node.js (v18+)
- Python (3.10+)
- A [Groq API Key](https://console.groq.com/keys)
- (Optional) Google Cloud OAuth `credentials.json` for Calendar Sync.

### 1. Backend Setup

Open a terminal and navigate to the backend folder:

```bash
cd backend
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate
# For Mac/Linux use: source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn groq pydantic langchain playwright bs4 pydantic-settings google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Install playwright browsers
playwright install chromium
```

**Environment Variables:**
Create a `.env` file in the `backend/` directory and add your Groq key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Start the Backend Server:**
```bash
uvicorn main:app --port 8000
```

### 2. Frontend Setup

Open a second terminal and navigate to the frontend folder:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Your frontend dashboard will now be running at `http://localhost:5173`.

---

## 📅 Setting up Google Calendar Sync (Optional)

If you want the "Sync to Calendar" button to actually create events:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Calendar API**.
3. Create OAuth 2.0 Client IDs (Desktop Application).
4. Download the JSON file, rename it to `credentials.json`, and place it in the `backend/` directory.

---
*Built with ❤️ for the Hackathon.*
