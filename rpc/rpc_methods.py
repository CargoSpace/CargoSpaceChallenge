from modernrpc.core import rpc_method

from contest.models import Contest, ContestProblem, ContestSubmission, AutoContestTitle, ContestSetting
from contest.models import ProblemSet, ProblemInput
from contest import views, lib as contest_lib
import time, moment
from datetime import date
import datetime

@rpc_method
def create_contest():
    contestSetting = ContestSetting.objects.all().first()
    if contestSetting.pauseAutomaticContest:
        return {'status': False, 'message': 'Automatic Contest Paused'}
    newContestProblem = contest_lib.getRandomObject(ProblemSet.objects.all())
    if not newContestProblem:
        return {'status': False, 'message': 'No contest problem found'}
    contestTitle = "Cargo_ Challenge"
    if contestSetting.useAutoContestTitle:
        autoContestTitle = contest_lib.getRandomObject(AutoContestTitle.objects.all())
        if not autoContestTitle:
            return {'status': False, 'message': 'No contest title found'}
        else:
            contestTitle = autoContestTitle.title
    start_time= moment.utcnow().clone()
    end_time = start_time.clone().add(minutes=int(contestSetting.duration))
    start_time = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hours, start_time.minutes, start_time.seconds)
    end_time = datetime.datetime(end_time.year, end_time.month, end_time.day, end_time.hours, end_time.minutes, end_time.seconds)
    print (start_time)
    print (end_time)
    # return
    newContest = Contest.objects.create(title=contestTitle, 
        start_time= start_time, 
        end_time= end_time,) #.format("YYYY-MM-DD HH:MM:ss"), )
    newContest.save()
    contestProblemSet = ContestProblem.objects.create(contest=newContest, problem=newContestProblem)
    contestProblemSet.save()
    return {'status': True, 'message': "Success"}