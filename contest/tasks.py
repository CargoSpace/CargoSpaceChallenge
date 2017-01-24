# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from celery import Celery
from celery.schedules import crontab
from rpc import rpc_methods
from . import lib

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
    'Execute-every-sixty-seconds': {
        'task': 'Hello World Task',
        'schedule': crontab(),
        'args': ('Hello World'),
    },
}

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

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
    

@shared_task(name="Create Submission")
def judge_submission(pk):
    logger.info("Start Judging Submission:")
    logger.info(pk)
    logger.info(lib.judge_submission(pk))
    logger.info("Finished Judging Submission Task:")
    return pk