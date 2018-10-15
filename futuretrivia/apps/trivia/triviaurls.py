from django.urls import path, re_path
from . import views



urlpatterns = [
	path('', views.triviaDetails, name='triviadetails'),
	path('leaderboard/', views.triviaLeaderboard, name='leaderboard'),
	path('getrankers/', views.getRankers, name='getrankers'),
	
]
