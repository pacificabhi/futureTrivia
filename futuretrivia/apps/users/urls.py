from django.urls import path, re_path, include
from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('authmail/', views.auth_mail, name='authmail'),
	path('settings/', include('apps.users.settingsurls')),
	path('signup/', views.userSignup, name='usersignup'),
	path('login/', views.userLogin, name='userlogin'),
	path('logout/', views.userLogout, name='userlogout'),
    path('registercontest/', views.registerContest, name='registercontest'),
    re_path('u/(?P<username>[a-z0-9_]{0,})/$', views.userProfile, name='userprofile'),
]
