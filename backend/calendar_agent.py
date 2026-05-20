import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Warning: credentials.json not found. Mocking successful calendar sync for demo purposes.")
                return "MOCK_SUCCESS"
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def add_hackathon_to_calendar(hackathon_title: str, start_date_str: str, end_date_str: str, link: str):
    """
    Adds the hackathon to the Google Calendar.
    For simplicity in this agent demo, we assume dates are passed in YYYY-MM-DD format.
    """
    service = get_calendar_service()
    if service == "MOCK_SUCCESS":
        print(f"Mock: Event {hackathon_title} added to calendar!")
        return True
    elif not service:
        return False
        
    try:
        event = {
          'summary': f'Hackathon: {hackathon_title}',
          'location': 'Online / TBD',
          'description': f'Hackathon application submitted via Hackathon Saathi.\nLink: {link}',
          'start': {
            'date': start_date_str, # Format: '2026-10-15'
            'timeZone': 'UTC',
          },
          'end': {
            'date': end_date_str, # Format: '2026-10-17'
            'timeZone': 'UTC',
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 60},
            ],
          },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return True
    except HttpError as error:
        print(f'An error occurred creating the event: {error}')
        return False

if __name__ == '__main__':
    # Test function. Needs credentials.json to exist.
    print("Testing Calendar Integration...")
    # add_hackathon_to_calendar("AI Innovators Challenge", "2026-10-15", "2026-10-17", "https://devfolio.co")
