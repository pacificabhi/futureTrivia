from django.urls import path, re_path
from . import views


urlpatterns = [
	path('', views.userSettings, name='usersettings'),
	path('resetpassword/', views.userResetPassword, name='resetpassword'),
	path('confirmemail/', views.userConfirmEmail, name='confirmemail'),
	path('account/', views.accountSettings, name='accountsettings'),
	path('security', views.securitySettings, name='securitysettings'),
]
