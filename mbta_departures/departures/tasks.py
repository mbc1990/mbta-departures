
import requests
import String.IO
import csv

from utils import update_departures

from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

@periodic_task(run_every=(crontab()), name="demo_task", ignore_result=True)
def fetch_departure_data():
    res = requests.get("http://developer.mbta.com/lib/gtrtfs/Departures.csv")
    if res.status_code == 200:
        f = StringIO.StringIO(res.content)
        reader = csv.reader(f, delimiter=',')

        # Truncate first row (contains field definitions)
        rows = list(reader)[1:]
        update_departures(rows)
    else:
        pass
