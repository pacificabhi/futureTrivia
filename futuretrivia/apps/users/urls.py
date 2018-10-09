from django.urls import path, re_path, include
from . import views



urlpatterns = [
	path('settings/', include('apps.users.settingsurls')),
	path('signup/', views.userSignup, name='usersignup'),
	path('login/', views.userLogin, name='userlogin'),
	path('logout/', views.userLogout, name='userlogout'),
    path('registercontest/', views.registerContest, name='registercontest'),
    path('', views.dashboard, name='dashboard'),
    re_path('(?P<username>[a-z0-9_]{0,})/$', views.userProfile, name='userprofile'),
]
