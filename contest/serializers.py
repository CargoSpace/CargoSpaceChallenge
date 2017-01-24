from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput
from rest_framework import serializers


class ContestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contest
		# fields = ('id')

class ProblemSetSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProblemSet
		# fields = ('id')
		# exclude = ('is_answer',)
		
class ContestSubmissionSerializer(serializers.ModelSerializer):
	contest = ContestSerializer(many=False, read_only=True)
	problem = ProblemSetSerializer(many=False, read_only=True)
	class Meta:
		model = ContestSubmission
		# fields = ('id')