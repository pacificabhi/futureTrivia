from django.shortcuts import render
from django.http import *
from django.urls import reverse
from .user_validation import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def userLogin(request):

	if(request.user.is_authenticated):
		return HttpResponseRedirect(reverse('userprofile', kwargs={'username':request.user.username}))

	if(request.method == "POST"):
		context={"success": True}
		errors=[]
		username = request.POST.get("username").strip().lower()
		password = request.POST.get("password")

		u=get_user(username)

		if not u:
			errors.append("No Account Found")
		elif not u.is_active:
			errors.append("Acount is deactivated. Contact us to activate it.")
		else:
			#print(u)
			u=authenticate(username=u.username, password=password)
			if not u:
				errors.append("Wrong Password")


		if errors:
			context["success"]=False
			context["errors"]=errors
			return JsonResponse(context)

		login(request, u)

		return JsonResponse(context)

	return render(request, 'users/login.html', {})

def userLogout(request):
	logout(request)
	return HttpResponseRedirect(reverse('userlogin'))


def userRegister(request):

	#print(request.user.is_authenticated)
	if(request.user.is_authenticated):
		return HttpResponseRedirect(reverse('userprofile', kwargs={'username':request.user.username}))

	if(request.method == "POST"):
		context={"success": True}
		errors=[]
		email = request.POST.get("email").strip().lower()
		username = request.POST.get("username").strip().lower()
		password = request.POST.get("password")

		if not validate_username(username):
			errors.append("Invalid Username")
		elif user_exists(username):
			errors.append("Username already taken")

		if not check_email_dns(email):
			errors.append("Invalid Email")
		elif user_exists(email):
			errors.append("Email already taken")

		if not validate_password(password):
			errors.append("Password must be 8 characters long")

		if errors:
			context["success"]=False
			context["errors"]=errors
			return JsonResponse(context)

		u = User.objects.create(username=username, email=email)
		u.set_password(password)
		u.save()

		login(request, u)

		return JsonResponse(context)

	return render(request, 'users/register.html', {})

def dashboard(request):

	return render(request, 'users/dashboard.html', {})


def userProfile(request, username):
	user=User.objects.filter(username=username).first()
	context={"exist":False, "active": False}
	if user:
		context["exist"]=True
		if user.is_active:
			context["active"]=True
			context["user"]=user



	return render(request, 'users/userProfile.html', context)