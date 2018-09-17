from django.db import models
from django.contrib.auth.models import User
from apps.trivia.models import Trivia



class UserDetails(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
	trivias = models.ManyToManyField(Trivia)
	security_question = models.CharField(max_length=100, blank=True, null=True)
	security_answer = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True, default="India")


	def __str__(self):
		return self.user.username
