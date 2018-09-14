from django.urls import path, re_path
from . import views



urlpatterns = [
	path('register/', views.userRegister, name='userregister'),
	path('login/', views.userLogin, name='userlogin'),
	path('logout/', views.userLogout, name='userlogout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    re_path('(?P<username>[a-z0-9_]{1,})/$', views.userProfile, name='userprofile'),
]
