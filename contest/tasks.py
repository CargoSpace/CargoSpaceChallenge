# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from celery import Celery
from celery.schedules import crontab
from . import lib

logger = get_task_logger(__name__)

# http://celery.readthedocs.io/en/latest/userguide/periodic-tasks.html
# http://docs.celeryproject.org/en/latest/userguide/configuration.html

app = Celery()
app.conf.timezone = 'UTC'

@shared_task(name="tasks.create_contest")
def create_contest():
    lib.create_contest()

# Called Every Second
@shared_task(name="tasks.compute_update_next_contest")
def compute_update_next_contest():
    next_contest = lib.compute_update_next_contest()
    logger.info(next_contest)
    

@app.task(name="tasks.test")
def test(arg):
    logger.info("Creating task:")
    print(arg)
    logger.info("Task finished:")

@shared_task(name="Create Submission")
def judge_submission(pk):
    logger.info("Start Judging Submission:")
    logger.info(pk)
    lib.judge_submission(pk)
    logger.info("Finished Judging Submission Task:")
    return pk