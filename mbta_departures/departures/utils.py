from models import Departure
from django.utils import timezone

def update_departures(departures):
    # Get existing departures by trip number
    # TODO: Only query as far back as a few days since trips should be gone by then
    existing_trips = Departure.objects.all()

    # TODO: Needs some optimization
    already_exist = [d for d in departures if d[2] in existing_trips]
    for dep in already_exist:
        obj = Departure.objects.filter(trip=dep[2])
        
        # TODO: Simplify?
        S = Departure
        api_status = d[7]
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
            pass
            # TODO: Throw exception
            

        obj.last_updated=timezone.datetime.fromtimestamp(int(dep[0]))
        obj.lateness=timezone.timedelta(seconds=int(dep[5]))
        obj.track=dep[6]
        obj.status=status
        obj.save()

    # Create new departures
    new = [d for d in departures if d[2] not in existing_trips]
    for dep in new:
        # TODO: Simplify
        S = Departure
        api_status = d[7]
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
