from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput

import random

def getRandomObject(problemSets):
    if problemSets and len(problemSets) > 0:
        return random.choice(problemSets);
    else:
        return None;
            