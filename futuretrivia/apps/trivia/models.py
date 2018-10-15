from django.db import models
from django.contrib.auth.models import User
import ast

# Create your models here.

class Trivia(models.Model):

	admin = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=False, null=False)
	code = models.CharField(max_length=20, blank=False, null=False, unique=True)
	password = models.CharField(max_length=40, blank=True, null=False, default="")
	category = models.CharField(max_length=100, blank=False, null=False, default="General")

	poster = models.CharField(max_length=2000, blank=True, null=False)
	quote = models.CharField(max_length=100, blank=True, null=False)
	prize = models.TextField(max_length=500, blank=False, null=False, default="Not Declared")
	about = models.TextField(blank=False, null=False, max_length=1000, default="No details.")
	announcements = models.TextField(blank=False, null=False, max_length=500, default="No Announcements")

	start_time = models.DateTimeField(blank=False, null=False)
	duration = models.IntegerField(blank=False, null=False, default=0)
	#per_questions_duration = models.IntegerField(blank=False, null=False, default=0)
	portal_duration = models.IntegerField(blank=False, null=False, default=0)


	#can_navigate = models.BooleanField(blank=False, null=False, default=False)
	can_change_answer = models.BooleanField(blank=False, null=False, default=False)
	individual_timing = models.BooleanField(blank=False, null=False, default=True)
	#question_timing = models.BooleanField(blank=False, null=False, default=True)
	live = models.BooleanField(blank=False, null=False, default=False)
	rated = models.BooleanField(blank=False, null=False, default=False)
	private = models.BooleanField(blank=False, null=False, default=False)
	


	def __str__(self):
		return self.code



class Question(models.Model):
	
	trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE)
	question = models.TextField(blank=False, null=False)
	mcq = models.BooleanField(blank=False, null=False, default=True)
	positive_score = models.IntegerField(blank=False, null=False, default=0)
	negative_score = models.IntegerField(blank=False, null=False, default=0)
	duration = models.IntegerField(blank=False, null=False, default=0)

	options = models.TextField(blank=False, null=False, default="{}")

	correct_answer = models.IntegerField(blank=False, null=False, default=0)

	explaination = models.TextField(blank=False, null=False, default = "No explaination")


	def __str__(self):
		return self.question



class TriviaResult(models.Model):

	trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	start_time = models.DateTimeField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)
	time_taken = models.IntegerField(blank=False, null=False, default=0)

	answers = models.TextField(blank=False, null=False, default="{}")

	positive_score = models.IntegerField(blank=False, null=False, default=0)
	negative_score = models.IntegerField(blank=False, null=False, default=0)
	#total_score = models.IntegerField(blank=False, null=False, default=0)


	def __str__(self):
		return self.user.username+'_'+self.trivia.code



	def calculate_score(self, questions_set):
		
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