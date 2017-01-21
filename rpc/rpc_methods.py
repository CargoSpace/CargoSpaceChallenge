from modernrpc.core import rpc_method

from contest.models import Contest, ContestProblem, ContestSubmission, AutoContestTitle, ContestSetting
from contest.models import ProblemSet, ProblemInput
from contest import views, lib as contest_lib
import time, moment
from datetime import date
import datetime
from django.utils import timezone

@rpc_method
def create_contest():
    contestSetting = ContestSetting.objects.all().first()
    if contestSetting.pauseAutomaticContest:
        print("cant proceed. flag automatic contest pausing..")
        return {'status': False, 'message': 'Automatic Contest Paused'}
    newContestProblem = contest_lib.getRandomObject(ProblemSet.objects.all())
    if not newContestProblem:
        print("no contest problem found")
        return {'status': False, 'message': 'No contest problem found'}
    contestTitle = "Cargo_ Challenge"
    if contestSetting.useAutoContestTitle:
        autoContestTitle = contest_lib.getRandomObject(AutoContestTitle.objects.all())
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