from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic

from .forms import AttendeeFormSet
from .models import Event, Attendee, CreatedEvent
from django.shortcuts import render, redirect

from myprofile.calender_api.create_calender_event import calendar_event


def homepage(request):
    event_ids = Event.objects.all().values('id')
    events = []
    for event in event_ids:
        event_data = {}
        event_data = Event.objects.filter(id=event['id']).values()[0]
        event_data['links'] = CreatedEvent.objects.filter(event_id = event['id']).values()
        # print(event_data)
        # print
        event_data['attendees'] = Attendee.objects.filter(event=event['id'])
        events.append(event_data)
    return render(request = request,
                  template_name='index.html',
                  context = {'events':events})


class EventCreate(generic.CreateView):
    model = Event
    fields = ['description', 'summary','start','end']


class EventAttendeeCreate(generic.CreateView):
    model = Event
    fields = ['description', 'summary','start','end']
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(EventAttendeeCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attendees'] = AttendeeFormSet(self.request.POST)
        else:
            data['attendees'] = AttendeeFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attendees = context['attendees']
        with transaction.atomic():
            t = self.object = form.save()
            event_data = Event.objects.filter(id=t.id).values()
            events = [event for event in event_data]
            attendees_dict = []
            if attendees.is_valid():
                attendees.instance = self.object
                attendees_data = attendees.save()
                attendees_dict = [{'email': attendee.email} for attendee in attendees_data]

            created_event = calendar_event(events[0],attendees_dict)

        return super(EventAttendeeCreate, self).form_valid(form)


class EventUpdate(generic.UpdateView):
    model = Event
    success_url = '/'
    fields = ['description', 'summary','start','end']


class EventAttendeeUpdate(generic.UpdateView):
    model = Event
    fields = ['description', 'summary','start','end']
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(EventAttendeeUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attendees'] = AttendeeFormSet(self.request.POST, instance=self.object)
        else:
            data['attendees'] = AttendeeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attendees = context['attendees']
        with transaction.atomic():
            self.object = t = form.save()
            event_data = Event.objects.filter(id=t.id).values()
            events = [event for event in event_data]
            attendees_dict = []
            if attendees.is_valid():
                attendees.instance = self.object
                attendees_data = attendees.save()
                attendees_dict = [{'email': attendee.email} for attendee in attendees_data]

            created_event = calendar_event(events[0],attendees_dict)

        return super(EventAttendeeUpdate, self).form_valid(form)


def EventDelete(request,id):
    Attendee.objects.filter(event=id).delete()
    Event.objects.filter(id=id).delete()
    # print("here")
    return redirect('index')