from django.shortcuts import render
from django.http import *
from django.urls import reverse
from .user_validation import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import UserDetails
from apps.trivia.models import Trivia
import pytz, datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

def dashboard(request):
	if True:
		return render(request,'trivia/not_found.html', {})
		
	return render(request, 'users/dashboard.html',{})

def userLogin(request):

	nxt = request.GET.get("next")


	if request.method == "POST":
		context = {"success": True, "loggedin": False}
		if request.user.is_authenticated:
			context["success"]=False
			context["loggedin"]=True
			return JsonResponse(context)
		errors = []
		username = request.POST.get("username").strip().lower()
		password = request.POST.get("password")

		u = get_user(username)

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

	if request.user.is_authenticated:
		if nxt:
			return HttpResponseRedirect(nxt)

		return HttpResponseRedirect(reverse('userprofile', kwargs={'username':request.user.username}))


	if not nxt:
		nxt=""
	return render(request, 'users/login.html', {"next":nxt})



def userLogout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def userSignup(request):

	#print(request.user.is_authenticated)


	nxt = request.GET.get("next")

	if request.method == "POST":
		context = {"success": True, "loggedin": False}
		if request.user.is_authenticated:
			context["success"]=False
			context["loggedin"]=True
			return JsonResponse(context)

		errors = []
		email = request.POST.get("email").strip().lower()
		username = request.POST.get("username").strip().lower()
		password = request.POST.get("password")

		if not validate_username(username):
			errors.append("Invalid Username")
		elif user_exists(username):
			errors.append("Username already taken")

		if user_exists(email):
			errors.append("Email already taken")
		elif not check_email_dns(email):
			errors.append("Invalid Email")

		if not validate_password(password):
			errors.append("Password must be 8 characters long")

		if errors:
			context["success"]=False
			context["errors"]=errors
			return JsonResponse(context)

		u = User.objects.create(username = username, email = email)
		u.set_password(password)
		u.save()

		ud = UserDetails.objects.create(user = u)

		login(request, u)

		return JsonResponse(context)

	if request.user.is_authenticated:

		if nxt:
			return HttpResponseRedirect(nxt)

		return HttpResponseRedirect(reverse('userprofile', kwargs={'username':request.user.username}))

	if not nxt:
		nxt=""
	
	return render(request, 'users/signup.html', {"next": nxt})


def userProfile(request, username):
	user = User.objects.filter(username=username).first()
	context ={}
	if user and user.is_active:
		context["profile"] = user
		recenttrivias = user.triviaresult_set.filter(time_taken__gt=0).order_by("-start_time")
		recentpractice = user.practiceresult_set.filter(time_taken__gt=0).order_by("-start_time")

		context["recenttrivias"]=recenttrivias
		context["recentpractice"]=recentpractice

	else:
		return render(request,'trivia/not_found.html', {})

	return render(request, 'users/userProfile.html', context)




@login_required
def userSettings(request):
	context={}

	return HttpResponseRedirect(reverse('accountsettings'))

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))


	return render(request, 'users/settings.html', context)

@login_required
def accountSettings(request):


	if request.method == "POST":
		errors = []
		context = {"success": True}
		if not request.user.is_authenticated:
			context["success"]=False
			errors.append("You are not loggedin")
			context["errors"]=errors
			return JsonResponse(context)

		fname = request.POST.get("fname").strip().title()
		lname = request.POST.get("lname").strip().title()
		email = request.POST.get("email").strip().lower()
		

		nerr = invalid_name(fname, lname)

		if nerr:
			errors.append(nerr)

		
		if request.user.email != email:
			if user_exists(email):
				errors.append("Email already taken")
			elif not check_email_dns(email):
				errors.append("Invalid Email")


		if errors:
			context["success"]=False
			context["errors"]=errors
			return JsonResponse(context)

		request.user.first_name = fname
		request.user.last_name = lname
		request.user.email = email

		request.user.save()
		context["success"] = True

		return JsonResponse(context)

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))
	
	context={"accountclass": "border-success", "accountset": True}


	return render(request, 'users/subsettings.html', context)

@login_required
def securitySettings(request):



	if request.method == "POST":
		errors = []
		context = {"success": True}

		if not request.user.is_authenticated:
			context["success"]=False
			errors.append("You are not loggedin")
			context["errors"]=errors
			return JsonResponse(context)

		cpass = request.POST.get("cpass")
		passwd = request.POST.get("pass")
		cnfpass = request.POST.get("cnfpass")
		
		if passwd != cnfpass:
			context["success"]=False
			errors.append("Confirm Password do not match")
			context["errors"]=errors
			return JsonResponse(context)

		if not validate_password(passwd):
			context["success"]=False
			errors.append("Password must be 8 characters long")
			context["errors"]=errors
			return JsonResponse(context)

		chk = authenticate(username=request.user.username, password=cpass)

		if not chk:
			context["success"]=False
			errors.append("Wrong Password")
			context["errors"]=errors
			return JsonResponse(context)

		request.user.set_password(passwd)
		request.user.save()

		new = authenticate(username=request.user.username, password=passwd)
		login(request, new)
		context["success"] = True

		return JsonResponse(context)

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))

	context={"securityclass": "border-success", "securityset": True}


	return render(request, 'users/subsettings.html', context)




@login_required
def socialSettings(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))


	if request.method == "POST":
		pass

	context={"socialclass": "border-success", "socialset": True}


	return render(request, 'users/subsettings.html', context)





@login_required
def additionalSettings(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))


	if request.method == "POST":
		pass

	context={"additionalclass": "border-success", "additionalset": True}


	return render(request, 'users/subsettings.html', context)
	



def registerContest(request):
	context={"success": False}

	if not request.user.is_authenticated:
		context["error"] = "Sign in to Register"
		return JsonResponse(context)

	code = request.GET.get("code")
	trivia = Trivia.objects.filter(code=code).first()
	
	if not trivia:
		context["error"] = "Trivia not found"
		return JsonResponse(context)

	now=datetime.datetime.now().replace(tzinfo=pytz.utc)
	portal_endtime = trivia.start_time + datetime.timedelta(seconds=trivia.portal_duration)

	if now > portal_endtime:
		context["error"] = "Registration ended"
		return JsonResponse(context)

	if not trivia.ready:
		context["error"] = "Trivia not ready"
		return JsonResponse(context)

	if trivia.admin == request.user:
		context["error"] = "You can not participate in this trivia"
		return JsonResponse(context)

	request.user.userdetails.trivias.add(trivia)
	context["success"] = True

	return JsonResponse(context)


	