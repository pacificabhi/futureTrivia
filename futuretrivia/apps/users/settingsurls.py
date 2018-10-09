from django.urls import path, re_path
from . import views


urlpatterns = [
	path('', views.userSettings, name='usersettings'),
	path('social/', views.socialSettings, name='socialsettings'),
	path('account/', views.accountSettings, name='accountsettings'),
	path('security', views.securitySettings, name='securitysettings'),
	path('additional', views.additionalSettings, name='additionalsettings'),
]
