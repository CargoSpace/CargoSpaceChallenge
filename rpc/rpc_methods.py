from modernrpc.core import rpc_method

from contest.models import Contest, ContestProblem, ContestSubmission, AutoContestTitle, ContestSetting
from contest.models import ProblemSet, ProblemInput
from contest import views, lib as contest_lib
import moment
from datetime import datetime

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
    now = moment.now()
    newContest = Contest.objects.create(title=contestTitle, 
        start_time= now.add(hour=int(contestSetting.interval)).date.strftime("%Y-%m-%d %H:%I:%S"), 
        end_time=now.add(hour=int(contestSetting.interval), minutes=contestSetting.duration).date.strftime("%Y-%m-%d %H:%I:%S"), )
    newContest.save()
    contestProblemSet = ContestProblem.objects.create(contest=newContest, problem=newContestProblem)
    contestProblemSet.save()
    return {'status': True, 'message': "Success"}