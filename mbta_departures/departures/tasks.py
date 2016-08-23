
from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

@periodic_task(run_every=(crontab()), name="demo_task", ignore_result=True)
def update_departures():
    pass
    # TODO: call departures API and handle database entry 
