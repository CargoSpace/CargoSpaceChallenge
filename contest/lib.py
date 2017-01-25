from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput
from django.contrib.auth.models import User
from .serializers import ContestSubmissionSerializer
import uuid
import random
import filecmp
from channels import Group
import json
import urllib


def getRandomObject(problemSets):
    if problemSets and len(problemSets) > 0:
        return random.choice(problemSets);
    else:
        return None;


def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = urllib.urlopen(filename).read()
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


def compareFiles(fileA, fileB):
    a = file_get_contents(fileA)
    b = file_get_contents(fileB)
    if [x for x in a if x not in b] == []:
        return True


def judge_submission(pk):
    contestSubmission = ContestSubmission.objects.get(pk=pk)
    # TODO: Jurge Here
    # contestSubmission.submission
    contestSubmission.submission_state = "Accepted"
    contestSubmission.save()
    smcontestSubmission = ContestSubmissionSerializer(contestSubmission, many=False)
    user = User.objects.get(pk=str(smcontestSubmission.data['submitted_by']))
    Group('user-' + user.username).send({'text': json.dumps({
        "response": smcontestSubmission.data,
        "messageType": "submission"
    })})
    return smcontestSubmission
    
def getUserSubmission(user_id, contest_id):
    contest_id = uuid.UUID(contest_id)
    contest = Contest.objects.get(pk=contest_id)
    user = User.objects.get(username=user_id)
    contestSubmission = ContestSubmission.objects.filter(submitted_by=user, contest=contest).order_by('-created_at')
    smcontestSubmission = ContestSubmissionSerializer(contestSubmission, many=True)
    return smcontestSubmission.data
    
    
