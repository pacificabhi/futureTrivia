from django.urls import path, re_path, include
from . import views


urlpatterns = [
	path('', views.hostedTrivia, name='hostedtrivia'),
	re_path('edit/(?P<code>[A-Z0-9_]{1,})/',views.editTrivia, name='edittrivia'),
	
]
