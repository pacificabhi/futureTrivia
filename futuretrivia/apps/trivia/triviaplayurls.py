from django.urls import path, re_path
from . import views



urlpatterns = [
	path('', views.triviaDetails, name='triviadetails'),
	path('play/', views.triviaPlay, name='triviaplay'),
	path('afteranswer/', views.afterAnswer, name='afteranswer'),
	path('useranswer/', views.userAnswer, name='useranswer'),
	path('leaderboard/', views.triviaLeaderboard, name='trivialeaderboard'),
	path('getrankers/', views.getRankers, name='getrankers'),
	path('start/', views.triviaStart, name='triviastart'),
	path('allquestions/', views.allTriviaQuestions, name='alltriviaquestions'),
	path('submitanswer/', views.submitAnswer, name='submitanswer'),
	path('endtest/', views.endTest, name='endtest'),
	path('triviastars/', views.triviaStars, name='triviastars'),
	
]
