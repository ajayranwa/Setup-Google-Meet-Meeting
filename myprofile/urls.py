from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('event/add/', views.EventAttendeeCreate.as_view(), name='event-add'),
    path('event/<int:pk>', views.EventAttendeeUpdate.as_view(), name='event-update'),
    path('event_delete/<id>', views.EventDelete, name='event-delete'),
]