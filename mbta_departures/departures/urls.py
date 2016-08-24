
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DepartureListView.as_view(), name='departures'),
    url(r'^poll_departures/$', views.get_latest_departures, name='poll_departures'),
]
