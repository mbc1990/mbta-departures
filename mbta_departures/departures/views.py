import json

from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse

from models import Departure

class DepartureListView(ListView):

    model = Departure 
    template_name = 'departures/departures_list.html'

    def get_context_data(self, **kwargs):
        context = super(DepartureListView, self).get_context_data(**kwargs)
        
        # TODO: When is a departure no longer needed?
        current_departures = Departure.objects.all()

        json_departures = []
        for dep in current_departures:
            json_departures.append({
                'origin':'Hell',
                'trip':'',
                'destination':'',
                'scheduled_time':'',
                'lateness':'',
                'track':'',
                'status':'',
            })
        context['json_departures'] = json.dumps(json_departures)
        return context
