from django.forms import ModelForm, inlineformset_factory

from .models import Event, Attendee


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ()


class AttendeeForm(ModelForm):
    class Meta:
        model = Attendee
        exclude = ()


AttendeeFormSet = inlineformset_factory(Event, Attendee,
                                            form=AttendeeForm, extra=1)