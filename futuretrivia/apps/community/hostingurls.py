from django.urls import path, re_path, include
from . import views


urlpatterns = [
	path('', views.hostedTrivia, name='hostedtrivia'),
	re_path('editquestion/(?P<code>[A-Z0-9_]{1,})/$', views.editQuestion, name='editquestion'),
	re_path('deletequestion/(?P<code>[A-Z0-9_]{1,})/$', views.deleteQuestion, name='deletequestion'),
	re_path('edit/(?P<code>[A-Z0-9_]{1,})/$',views.editTrivia, name='edittrivia'),
	re_path('questions/(?P<code>[A-Z0-9_]{1,})/$',views.hostedTriviaQuestions, name='hostedtriviaquestions'),
]
