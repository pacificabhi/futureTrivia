from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trivia(models.Model):

	admin=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=100, blank=False, null=False)
	code=models.CharField(max_length=20, blank=False, null=False, unique=True)
	prize=models.TextField(max_length=500, blank=False, null=False, default="Not Declared")
	about=models.TextField(blank=False, null=False, max_length=1000, default="No details.")
	announcements=models.TextField(blank=False, null=False, max_length=500, default="No Announcements")
	start_time=models.DateTimeField(blank=False, null=False)
	duration=models.IntegerField(blank=False, null=False, default=0)
	per_problem_duration=models.IntegerField(blank=False, null=False, default=0)
	positive_score=models.IntegerField(blank=False, null=False)
	negative_score=models.IntegerField(blank=False, null=False)
	can_navigate=models.BooleanField(blank=False, null=False, default=False)
	portal=models.BooleanField(blank=False, null=False, default=True)
	rated=models.BooleanField(blank=False, null=False, default=False)
	private=models.BooleanField(blank=False, null=False, default=False)
	category=models.CharField(max_length=100, blank=False, null=False, default="General")


	def __str__(self):
		return self.quiz_code
