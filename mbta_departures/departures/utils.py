from models import Departure
from django.utils import timezone

class UnexpectedStatusException(Exception):
    pass

def status_map(api_status):
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
        # TODO Test this exception 
        raise UnexpectedStatusException("Unexpected status from API: {0}".format(api_status))
    return status



def update_departures(departures):

    # Everything currently displayed 
    existing_trips = Departure.objects.filter(active=True)

    # Expire trips that are no longer returned by the API 
    newly_inactive = [d[2] for d in departures if d[2] in existing_trips.values_list('trip', flat=True)] 
    newly_inactive.update(active=False)
    
    # Reflect altereted active status 
    existing_trips.refresh_from_db()

    # TODO: Needs some optimization
    already_exist = [d for d in departures if d[2] in existing_trips.values_list('trip', flat=True)]
    for dep in already_exist:
        obj = Departure.objects.get(trip=dep[2])
        S = Departure
        api_status = d[7]
        status = status_map(api_status)
        obj.last_updated=timezone.datetime.fromtimestamp(int(dep[0]))
        obj.lateness=timezone.timedelta(seconds=int(dep[5]))
        obj.track=dep[6] or None
        obj.status=status
        obj.save()

    # Create new departures
    new = [d for d in departures if d[2] not in existing_trips.values_list('trip', flat=True)]
    for dep in new:
        # TODO: Simplify
        S = Departure
        api_status = d[7]
        status = status_map(api_status)
        Departure.objects.create(
            last_updated=timezone.datetime.fromtimestamp(int(dep[0])),
            trip=dep[2],
            origin=dep[1],
            destination=dep[3],
            scheduled_time= timezone.datetime.fromtimestamp(int(dep[4])),
            lateness=timezone.timedelta(seconds=int(dep[5])),
            track=dep[6] or None,
            status=status,
        )
