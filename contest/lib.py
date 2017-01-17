from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput

import random

def getRandomObject(problemSets):
    if len(problemSets):
        return random.sample(problemSets, 1)[0];
    else:
        return None;
            