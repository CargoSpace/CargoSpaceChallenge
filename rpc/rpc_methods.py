from modernrpc.core import rpc_method

from contest.models import Contest, ContestProblem, ContestSubmission, AutoContestTitle, ContestSetting
from contest.models import ProblemSet, ProblemInput
from contest import views, lib as contest_lib
import time, moment
from datetime import datetime, date

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
        autoContestTitle = contest_lib.getRandomObject(AutoContestTitle.objects.all());
        if not autoContestTitle:
            return {'status': False, 'message': 'No contest title found'}
        else:
            contestTitle = autoContestTitle.title
    newContest = Contest.objects.create(title=contestTitle, 
        start_time= moment.now().add(hours=int(contestSetting.interval)).date.strftime("%Y-%m-%d %H:%I:%S"), 
        end_time=moment.now().add(hours=int(contestSetting.interval)).add(minutes=30).date.strftime("%Y-%m-%d %H:%I:%S"),) #.format("YYYY-MM-DD HH:MM:ss"), )
    newContest.save()
    contestProblemSet = ContestProblem.objects.create(contest=newContest, problem=newContestProblem)
    contestProblemSet.save()
    return {'status': True, 'message': "Success"}