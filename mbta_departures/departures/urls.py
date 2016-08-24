
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DepartureListView.as_view(), name='departures'),
]
