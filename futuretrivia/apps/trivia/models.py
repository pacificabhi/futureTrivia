from django.db import models
from django.contrib.auth.models import User

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
	question_timing = models.BooleanField(blank=False, null=False, default=True)
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

	options = models.TextField(blank=False, null=False, default='')

	correct_answer = models.IntegerField(blank=False, null=False, default=0)

	explaination = models.TextField(blank=False, null=False, default = "No explaination")


	def __str__(self):
		return self.question



class TriviaResult(models.Model):

	trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE)
	username = models.ForeignKey(User,on_delete=models.CASCADE)

	start_time = models.DateTimeField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)

	answers = models.TextField(blank=False, null=False, default="")

	score = models.IntegerField(blank=False, null=False, default=0)


	def __str__(self):
		return self.username.username+'_'+self.trivia.code