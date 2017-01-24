from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput
from django.contrib.auth.models import User
from .serializers import ContestSubmissionSerializer
import uuid
import random
import filecmp

def getRandomObject(problemSets):
    if problemSets and len(problemSets) > 0:
        return random.choice(problemSets);
    else:
        return None;
        
def compareStdInAndStdOut(stdin, stdout):
    return filecmp.cmp(stdin, stdout)
    
def judge_submission(pk):
    contestSubmission = ContestSubmission.objects.get(pk=pk)
    return contestSubmission
    
def getUserSubmission(user_id, contest_id):
    contest_id = uuid.UUID(contest_id)
    contest = Contest.objects.get(pk=contest_id)
    user = User.objects.get(username=user_id)
    contestSubmission = ContestSubmission.objects.filter(submitted_by=user, contest=contest)
    smcontestSubmission = ContestSubmissionSerializer(contestSubmission, many=True)
    return smcontestSubmission.data
    
    
            