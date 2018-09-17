from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trivia(models.Model):

	admin = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=False, null=False)
	code = models.CharField(max_length=20, blank=False, null=False, unique=True)
	poster = models.CharField(max_length=2000, blank=True, null=False)
	quote = models.CharField(max_length=100, blank=True, null=False)
	prize = models.TextField(max_length=500, blank=False, null=False, default="Not Declared")
	about = models.TextField(blank=False, null=False, max_length=1000, default="No details.")
	announcements = models.TextField(blank=False, null=False, max_length=500, default="No Announcements")
	start_time = models.DateTimeField(blank=False, null=False)
	duration = models.IntegerField(blank=False, null=False, default=0)
	portal_duration = models.IntegerField(blank=False, null=False, default=0)
	per_problem_duration = models.IntegerField(blank=False, null=False, default=0)
	positive_score = models.IntegerField(blank=False, null=False, default=0)
	negative_score = models.IntegerField(blank=False, null=False, default=0)
	can_navigate = models.BooleanField(blank=False, null=False, default=False)
	portal = models.BooleanField(blank=False, null=False, default=True)
	live = models.BooleanField(blank=False, null=False, default=False)
	rated = models.BooleanField(blank=False, null=False, default=False)
	private = models.BooleanField(blank=False, null=False, default=False)
	password = models.CharField(max_length=40, blank=True, null=False, default="")
	category = models.CharField(max_length=100, blank=False, null=False, default="General")


	def __str__(self):
		return self.code

