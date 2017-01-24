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
        
def compareFiles(fileA, fileB):
    # compareFiles("/home/retnan/file.txt" "/home/retnan/file2.txt")
    # compareFiles("http://retnan.com/file.txt" "/home/retnan/file2.txt")
    return filecmp.cmp(fileA, fileB)
    
def judge_submission(pk):
    contestSubmission = ContestSubmission.objects.get(pk=pk)
    return contestSubmission
    
def getUserSubmission(user_id, contest_id):
    contest_id = uuid.UUID(contest_id)
    contest = Contest.objects.get(pk=contest_id)
    user = User.objects.get(username=user_id)
    contestSubmission = ContestSubmission.objects.filter(submitted_by=user, contest=contest).order_by('-created_at')
    smcontestSubmission = ContestSubmissionSerializer(contestSubmission, many=True)
    return smcontestSubmission.data
    
    
            