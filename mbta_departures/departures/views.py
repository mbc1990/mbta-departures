from django.http import JsonResponse
from django.views.generic import TemplateView
from utils import get_json_departures
from models import Departure

def get_latest_departures(request):
    return JsonResponse({'departures':get_json_departures()})

class DepartureListView(TemplateView):
    template_name = 'departures/departures_list.html'

    def get_context_data(self, **kwargs):
        context = super(DepartureListView, self).get_context_data(**kwargs)
        context['json_departures'] = get_json_departures()
        return context
