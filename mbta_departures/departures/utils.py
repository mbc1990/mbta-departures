import json
from models import Departure
from django.utils import timezone

class UnexpectedStatusException(Exception):
    pass

def status_map(api_status):
    '''
    Translate API responses into status enum values
    '''
    S = Departure
    if api_status == "On Time":
        status = S.STATUS_ON_TIME
    elif api_status == "Cancelled":
        status = S.STATUS_CANCELLED
    elif api_status == "Arriving":
        status = S.STATUS_ARRIVING
    elif api_status == "End":
        status = S.STATUS_END
    elif api_status == "Now Boarding":
        status = S.STATUS_NOW_BOARDING
    elif api_status == "Info to Follow":
        status = S.STATUS_INFO_TO_FOLLOW
    elif api_status == "Arrived":
        status = S.STATUS_ARRIVED
    elif api_status == "All Aboard":
        status = S.STATUS_ALL_ABOARD
    elif api_status == "TBD":
        status = S.STATUS_TBD
    elif api_status == "Departed":
        status = S.STATUS_DEPARTED
    elif api_status == "Delayed":
        status = S.STATUS_DELAYED
    elif api_status == "Late":
        status = S.STATUS_LATE
    elif api_status == "Hold":
        status = S.STATUS_HOLD
    else:
        raise UnexpectedStatusException("Unexpected status from API: {0}".format(api_status))
    return status

def update_departures(departures):

    # Expire old departures
    active_trip_ids = [d[2] for d in departures]
    now_inactive = Departure.objects.filter(active=True).exclude(trip__in=active_trip_ids)
    now_inactive.update(active=False)

    # Figure out which entries are going to be updated and which need to be created
    to_update = Departure.objects.filter(active=True, trip__in=active_trip_ids)
    to_update_ids = to_update.values_list('trip', flat=True)
    to_update_map = dict((el.trip, el) for el in list(to_update))

    # Iterate over the API response, updating and creating as necessary 
    for dep in departures:
        trip = dep[2]
        api_status = dep[7]
        status = status_map(api_status)
        if trip in to_update_map:
            obj = to_update_map[trip]
            obj.scheduled_time=timezone.datetime.fromtimestamp(int(dep[4]))
            obj.last_updated=timezone.datetime.fromtimestamp(int(dep[0]))
            obj.lateness=timezone.timedelta(seconds=int(dep[5]))
            obj.track=dep[6] or None
            obj.status=status
            obj.save()
        else:
            Departure.objects.create(
                last_updated=timezone.datetime.fromtimestamp(int(dep[0])),
                trip=dep[2],
                origin=dep[1],
                destination=dep[3],
                scheduled_time=timezone.datetime.fromtimestamp(int(dep[4])),
                lateness=timezone.timedelta(seconds=int(dep[5])),
                track=dep[6] or None,
                status=status,
            )

# TODO: Caching layer via redis, probably beyond the scope of this project... 
def get_json_departures():
    current_departures = Departure.objects.filter(active=True)
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
    return json.dumps(json_departures)
