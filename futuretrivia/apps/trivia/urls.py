from django.urls import path, re_path, include
from . import views



urlpatterns = [
	path('', views.triviaGames, name='triviahome'),
	re_path('compete/(?P<code>[A-Z0-9_]{1,})/', include('apps.trivia.triviaplayurls')),
	re_path('(?P<code>[A-Z0-9_]{1,})/', include('apps.trivia.triviaurls')),
]
