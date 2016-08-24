from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse

from models import Departure

class DepartureListView(ListView):

    model = Departure 
    template_name = 'departures/departures_list.html'

    def get_queryset(self):
        # TODO: How long to keep "departed" trains around for? 
        return Departure.objects.all()

    '''
    def get_context_data(self, **kwargs):
        context = super(DepartureListView, self).get_context_data(**kwargs)
        return context
    '''
