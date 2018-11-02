from django.db import models
from django.contrib.auth.models import User
from apps.trivia.models import Trivia



class UserDetails(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
	trivias = models.ManyToManyField(Trivia)
	confirmed = models.BooleanField(blank=False, null=False, default=False)
	confirm_token = models.CharField(max_length=256 ,blank=True, null=False, default="")
	
	emails = models.TextField(blank=False, null=False, default="{}")
	country = models.CharField(max_length=100, blank=True, null=True, default="India")



	def __str__(self):
		return self.user.username

	def is_account_confirmed(self):
	
		return self.confirmed
