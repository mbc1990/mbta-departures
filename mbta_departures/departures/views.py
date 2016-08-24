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
        # Probably when the API stops sending it
        current_departures = Departure.objects.all()

        json_departures = []
        for dep in current_departures:
            json_departures.append({
                'origin': dep.origin,
                'trip': dep.trip,
                'destination': dep.destination,
                'scheduled_time': dep.scheduled_time.isoformat(),
                'lateness': dep.lateness.seconds,
                'track': dep.track,
                'status': dep.get_status_display()
            })
        context['json_departures'] = json.dumps(json_departures)
        return context
