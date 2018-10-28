from django.urls import path, include, re_path
from .import views

urlpatterns = [
	path('', views.practiceHome, name='practicehome'),
	path('play/', views.practicePlay, name='practiceplay'),
	path('start/', views.practiceStart, name='practicestart'),
	path('allquestions/', views.allPracticeQuestion, name='allpracticequestions'),
	path('submitanswer/', views.submitPracticeAnswer, name='submitpracticeanswer'),
	path('endtest/', views.endPracticeTest, name='endpracticetest'),
	path('result/', views.practiceResult, name='practiceresult'),

]
