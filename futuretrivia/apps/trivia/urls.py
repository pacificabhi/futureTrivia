from django.urls import path, re_path
from . import views



urlpatterns = [
	path('', views.triviaGames, name='triviahome'),
	re_path('(?P<code>[A-Z0-9_]{1,})/$', views.triviaDetails, name='triviadetails'),
]
