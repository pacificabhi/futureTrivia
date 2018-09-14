from django.urls import path
from . import views



urlpatterns = [
	path('', views.triviaGames, name='triviahome'),
]
