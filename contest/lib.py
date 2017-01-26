from contest.models import Contest, ContestProblem, ContestSubmission, AutoContestTitle, ContestSetting
from contest.models import ProblemSet, ProblemInput
from django.contrib.auth.models import User
from .serializers import ContestSubmissionSerializer
import uuid
import random
import filecmp
from channels import Group
import json
import requests
from django.conf import settings
import os
from celery import Celery
import time, moment, datetime
from django.utils import timezone
import shelve

# Ported from JS: https://github.com/CargoSpace/ContestCreator/blob/master/lib.js
def getUpperHour(hour_set, hour):
	for i in range(0, len(hour_set)):
		for j in range(i + 1, i + 2):
			if i == (len(hour_set) - 1):
				return hour_set[0]
			if hour >= hour_set[i] and hour < hour_set[j]:
				return hour_set[j]
				
def compute_update_next_contest():
    Cache = shelve.open("AppSettings", writeback=True)
    if "Settings" in Cache: # Is this the best way to do caching in django?
        Settings = Cache['Settings']
    else:
        Settings = ContestSetting.objects.all().first()
        Cache['Settings'] = Settings
    contest_interval = Settings.interval
    hour_set = range(0, 24, contest_interval)
    if contest_interval is None:
        return
    now = moment.utcnow().clone()
    nextHour = getUpperHour(hour_set, now.hours)
    if nextHour == 0:
        now = now.clone().add(day=1)
    next_contest = str(now.year) + '-' + str(now.month) + '-' + now.day + ' ' + str(nextHour) + ':00:' + '00'
    Cache['next_contest'] = next_contest
    Cache.sync()
    Cache.close()
    return next_contest

def create_contest():
    contestSetting = ContestSetting.objects.all().first()
    if contestSetting.pauseAutomaticContest:
        print("cant proceed. flag automatic contest pausing..")
        return {'status': False, 'message': 'Automatic Contest Paused'}
    newContestProblem = getRandomObject(ProblemSet.objects.all())
    if not newContestProblem:
        print("no contest problem found")
        return {'status': False, 'message': 'No contest problem found'}
    contestTitle = "Cargo_ Challenge"
    if contestSetting.useAutoContestTitle:
        autoContestTitle = getRandomObject(AutoContestTitle.objects.all())
        if not autoContestTitle:
            print("no contest title found, disable autocontest title in settings")
            return {'status': False, 'message': 'No contest title found'}
        else:
            contestTitle = autoContestTitle.title
    start_time= moment.utcnow().clone()
    end_time = start_time.clone().add(minutes=int(contestSetting.duration))
    start_time = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hours, start_time.minutes, start_time.seconds)
    end_time = datetime.datetime(end_time.year, end_time.month, end_time.day, end_time.hours, end_time.minutes, end_time.seconds)

    newContest = Contest.objects.create(title=contestTitle, 
        start_time= start_time.replace(tzinfo=timezone.UTC()), 
        end_time= end_time.replace(tzinfo=timezone.UTC()),)
    newContest.save()
    contestProblemSet = ContestProblem.objects.create(contest=newContest, problem=newContestProblem)
    contestProblemSet.save()
    return {'status': True, 'message': "Success"}
    
def getRandomObject(problemSets):
    if problemSets and len(problemSets) > 0:
        return random.choice(problemSets);
    else:
        return None;

def get_celery_worker_status():
    ERROR_KEY = "ERROR"
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            d = { ERROR_KEY: 'No running Celery workers were found.' }
    except IOError as e:
        from errno import errorcode
        msg = "Error connecting to the backend: " + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the Redis server is running.'
        d = { ERROR_KEY: msg }
    except ImportError as e:
        d = { ERROR_KEY: str(e)}
    return d

def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = requests.get(filename).text
        if (offset > 0):
            ret = ret[offset:]
        if (maxlen > 0):
            ret = ret[:maxlen]
        return ret
    else:
        fp = open(filename,'rb')
        try:
            if (offset > 0):
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret
        finally:
            fp.close( )


def isEqual(fileA, fileB):
    a = file_get_contents(fileA)
    b = file_get_contents(fileB)
    if [x for x in a if x not in b] == []:
        return True
    else:
        return False
    
def judge_submission(pk):
    contestSubmission = ContestSubmission.objects.get(pk=pk)
    problemInput = ProblemInput.objects.filter(problem=contestSubmission.problem).first()
    cargoSpaceStdOutFile = problemInput.problem_stdout.path
    if os.path.isfile(cargoSpaceStdOutFile) is False:
        cargoSpaceStdOutFile = problemInput.problem_stdout.url #TODO: Concatenate with base url
    userStdOutFile = contestSubmission.submission.path
    if os.path.isfile(cargoSpaceStdOutFile) is False:
        userStdOutFile = contestSubmission.submission.url #TODO: Concatenate with base url

    if isEqual(str(cargoSpaceStdOutFile), str(userStdOutFile)):
        contestSubmission.submission_state = "Accepted"
    else:
        contestSubmission.submission_state = "Failed"
    contestSubmission.save()
    sContestSubmission = ContestSubmissionSerializer(contestSubmission, many=False)
    pushNotify(sContestSubmission)
    return sContestSubmission

def pushNotify(sContestSubmission):
    user = User.objects.get(pk=str(sContestSubmission.data['submitted_by']))
    Group('user-' + user.username).send({'text': json.dumps({
        "response": sContestSubmission.data,
        "messageType": "submission"
    })})
    
def getUserSubmission(user_id, contest_id):
    contest_id = uuid.UUID(contest_id)
    contest = Contest.objects.get(pk=contest_id)
    user = User.objects.get(username=user_id)
    contestSubmission = ContestSubmission.objects.filter(submitted_by=user, contest=contest).order_by('-created_at')
    smcontestSubmission = ContestSubmissionSerializer(contestSubmission, many=True)
    return smcontestSubmission.data
    
    
