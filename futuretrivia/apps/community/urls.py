from django.urls import path, re_path, include
from . import views


urlpatterns = [
	path('', views.communityHome, name='communityhome'),
	path('trivia/', include('apps.community.hostingurls')),
]
