#Create Google Meet Meeting with Django inline formset
==================

This is a simple django app that demonstrates how to create a Google Meet meeting with attendees.

###Prerequisites
-------------

To run this quickstart, you'll need:

1. Python 2.6 or greater
2. The pip package management tool
4. A Google account with Google Calendar enabled

###Step 1: Turn on the Google Calendar API
---------------------------------------
Visit the link(https://developers.google.com/calendar/quickstart/python) and **Enable the Google Calendar API** 

In resulting dialog click **DOWNLOAD CLIENT CONFIGURATION** and save the file credentials.json to *myprofile/calender_api/*.

###Quick start
-----------
1. (optional) create virtual env
2. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver 
