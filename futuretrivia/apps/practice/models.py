from django.db import models
from django.contrib.auth.models import User
from apps.trivia.models import Trivia
import ast

# Create your models here.


class PracticeResult(models.Model):

	trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	start_time = models.DateTimeField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)
	time_taken = models.IntegerField(blank=False, null=False, default=0)

	answers = models.TextField(blank=False, null=False, default="{}")

	positive_score = models.IntegerField(blank=False, null=False, default=0)
	negative_score = models.IntegerField(blank=False, null=False, default=0)
	stars = models.IntegerField(blank=False, null=False, default=0)


	def __str__(self):
		return self.user.username+'_'+self.trivia.code



	def calculate_score(self, questions_set=None):

		if self.submitted():
			return None

		if not questions_set:
			questions_set = self.trivia.question_set.all()
		
		answers = ast.literal_eval(self.answers)

		for ques in questions_set:
			if ques.id in answers.keys() and answers[ques.id]["opt_id"]!=0:

				if ques.correct_answer == answers[ques.id]["opt_id"]:
					self.positive_score+=ques.positive_score
				else:
					self.negative_score+=ques.negative_score

		#self.total_score = self.positive_score - self.negative_score



	def get_score(self):

		return self.positive_score - self.negative_score

	def submitted(self):

		return self.time_taken

