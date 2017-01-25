from contest.models import Contest, ContestProblem, ContestSubmission
from contest.models import ProblemSet, ProblemInput
from rest_framework import serializers


class ContestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contest
		# fields = ('id')
		fields = '__all__'

class ProblemInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProblemInput
		# fields = ('id')
		fields = '__all__'

class ProblemSetSerializer(serializers.ModelSerializer):
	problem_inputs = ProblemInputSerializer(many=True, read_only=True)
	class Meta:
		model = ProblemSet
		# fields = ('id')
		# exclude = ('is_answer',)
		fields = '__all__'
		
class ContestSubmissionSerializer(serializers.ModelSerializer):
	contest = ContestSerializer(many=False, read_only=True)
	problem = ProblemSetSerializer(many=False, read_only=True)
	class Meta:
		model = ContestSubmission
		# fields = ('id')
		fields = '__all__'