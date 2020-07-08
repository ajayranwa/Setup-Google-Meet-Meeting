from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from myprofile.models import Event, CreatedEvent

# If modifying these scopes, delete the file token.pickle.



def calendar_event(event_data,attendees):

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    """Shows basic usage of the Google Calendar API.

    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    pickle_file = 'myprofile/calender_api/token.pickle'
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'myprofile/calender_api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    

    event = {
        'summary': event_data['summary'],
        'description': event_data['description'],
        'start': {
            'dateTime': event_data['start'], 
            'timeZone': 'Asia/Kolkata'
        }, 
        'end': {
            'dateTime': event_data['end'], 
            'timeZone': 'Asia/Kolkata'
        },
        'attendees': attendees,
        'reminders': {
            'useDefault': True
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    # print ('Event created: %s' % (event.get('id')))
    # print("Google Meet Link:%s" %(event.get('hangoutLink')),"\n\n")

    event_id = Event.objects.get(id=event_data['id'])
    CreatedEvent.objects.filter(event_id=event_id).delete()
    t = CreatedEvent(event_id=event_id,htmlLink=event.get('htmlLink'),hangoutLink=event.get('hangoutLink'))
    t.save()

    # print(Event.objects.filter(id=event_data['id']).values())

    return event

