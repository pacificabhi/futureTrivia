from django.urls import path, include, re_path
from .import views

urlpatterns = [
	path('', views.aboutHome, name='abouthome'),
	path('codeofconduct/', views.codeOfConduct, name='codeofconduct'),

]
