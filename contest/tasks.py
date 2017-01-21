# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from celery import Celery
from celery.schedules import crontab
from rpc import rpc_methods

logger = get_task_logger(__name__)
app = Celery()
app.conf.timezone = 'UTC'

# For more crontab rules: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#beat-custom-schedulers
app.conf.beat_schedule = {
    # Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm.
    'Execute-every-three-hours': {
        'task': 'Create Contest',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': (),
    },
}

@shared_task(name="Create Contest")
def create_contest():
    logger.info("Creating task:")
    rpc_methods.create_contest()
    logger.info("Task finished:")

@app.task(name="Hello World Task")
def test(arg):
    logger.info("Creating task:")
    print(arg)
    logger.info("Task finished:")