from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput

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
    
    
            