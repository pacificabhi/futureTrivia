from django.shortcuts import render
from django.http import *
from django.urls import reverse
from .user_validation import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import UserDetails, FbUser
from apps.trivia.models import Trivia
import pytz, datetime
from django.contrib.auth.decorators import login_required
from .utility import *
import json, requests

# Create your views here.

#proxies = {'http': 'http://edcguest:edcguest@172.31.102.29:3128','https': 'https://edcguest:edcguest@172.31.102.29:3128','ftp': 'ftp://edcguest:edcguest@172.31.102.29:3128'}
proxies=None

def fbUserLogin(request):

	if request.user.is_authenticated:
		return JsonResponse({"success": True})

	context={"success": False}
	u=request.POST.get("user")
	u=json.loads(u)
	access_token=u["authResponse"]["accessToken"]
	uid=u["authResponse"]["userID"]
	url = "https://graph.facebook.com/%s?redirect=false&access_token=%s&fields=email,name"%(uid, access_token)
	r=requests.get(url, proxies=proxies)
	j=json.loads(r.content.decode('ascii'))

	if "error" in j.keys():
		context["error"]="Invalid Login"
		return JsonResponse(context)

	name=j["name"].strip().split()
	fname=name[0]
	lname=""
	if len(name)>1:
		lname=name[-1]

	email=""
	if "email" in j.keys():
		email = j["email"]

	if user_exists(email):
		email=""

	#check if first timer
	fbuser = FbUser.objects.filter(uid=uid).first()
	if fbuser:
		login(request,fbuser.user)
		context["success"]=True
		return JsonResponse(context)


	usr = User.objects.create(username=uid, email=email, first_name=fname, last_name=lname)
	ud = UserDetails.objects.create(user=usr, confirmed=True, auth_base=2)
	fbuser = FbUser.objects.create(user=usr, uid=uid)
	login(request, usr)
	context["success"] = True

	return JsonResponse(context)

def dashboard(request):
	if True:
		return render(request,'trivia/not_found.html', {})
		
	return render(request, 'users/dashboard.html',{})

@login_required
def userConfirmEmail(request):

	action = request.GET.get("action")

	if not action:
		return render(request, 'trivia/not_found.html', {})

	context = {}

	if action == 'sendconfirmationemail':

		ud = request.user.userdetails

		if not ud.confirmed:
			res = send_email_confirmation_mail(request.get_host(), ud, request.user.email)
			if res:
				context["email_resend"] = True
			else:
				context["error"] = "Please try again"

		else:
			context["error"] = "Your Email is already confirmed"
			context["already"] = True

	elif action == 'confirmemail':
		token = request.GET.get("token")
		if not request.user.is_authenticated:
			nxt = reverse('confirmemail')+"?action=confirmmail&token="+token
			return HttpResponseRedirect(reverse('userlogin')+nxt)


		ud = request.user.userdetails

		if ud.confirm_token == token:
			ud.confirmed = True
			ud.confirm_token = ""
			ud.save()
			context["email_confirmed"] = True

		else:
			context["error"] = "Invalid link or link expired"

	else:
		return render(request, 'trivia/not_found.html', {})

	
	return render(request, 'users/confirmemail.html', context)


def userResetPassword(request):
	
	action = request.GET.get("action")

	if request.is_ajax() and action == "sendresetmail":
		context = {"success": False}

		if request.user.is_authenticated:
			context["error"] = "already logged in"
			context["already"] = True
			return JsonResponse(context)

		username = request.GET.get("username").strip()
		user = get_user(username)

		if not user:
			context["error"] = "No account found"
			return JsonResponse(context)

		auth_base = user.userdetails.auth_base

		if auth_base!=1:
			if auth_base==2:
				context["error"] = "Your account is connected to facebook. You cannot change your password. Use facebook to login"
			
			return JsonResponse(context)			

		if not user.userdetails.is_account_confirmed():
			context["error"] = "Your email address is not confirmed. Please contact us at </b>futuretrivia@gmail.com</b>"
			return JsonResponse(context)

		res = send_password_reset_mail(user)
		if not res:
			context["error"] = "Something went wrong. Please try after sometime"
			return JsonResponse(context)

		context["success"] = True
		context["success_msg"] = "<span class='text-success'>&#10004; New Password is sent to you registered email address. Please check your inbox for new password and change it after you first log in</span><br><br><a class='btn btn-sm auth-btn' href='/users/login/'>Log in</a>"
		return JsonResponse(context)


	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('triviahome'))

	return render(request, 'users/reset_password.html', {})

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
			auth_base = u.userdetails.auth_base
			if auth_base!=1:
				errors.append("Invalid Login")
				if auth_base==2:
					errors.append("Your account is linked with facebook. Please use facebook to login into your account")
			else:
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

		send_email_confirmation_mail(request.get_host(), ud, email)
				
		
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

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))

	tab = request.GET.get("tab")
	
	if tab == 'account':
		context["accounttab"]=True
	elif tab == 'security':
		context["securitytab"]=True
	else:
		context["accounttab"]=True

	return render(request, 'users/settings.html', context)

@login_required
def accountSettings(request):
	context = {"success": False}

	if request.method == "POST":
		errors = []
		if not request.user.is_authenticated:
			errors.append("You are not logged in")
			context["errors"]=errors
			return JsonResponse(context)

		settype = request.POST.get("settype")

		if settype == "fullname":

			fname = request.POST.get("fname").strip().title()
			lname = request.POST.get("lname").strip().title()
			uname = request.POST.get("uname").strip().lower()

			if uname!=request.user.username:
				if not validate_username(uname):
					errors.append("Invalid Username")
				elif user_exists(uname):
					errors.append("Username already taken")
			
			nerr = invalid_name(fname, lname)

			if nerr:
				errors.append(nerr)
			
			if errors:
				context["errors"]=errors
				return JsonResponse(context)

			request.user.first_name = fname
			request.user.last_name = lname
			request.user.username = uname
			request.user.save()
			context["success"] = True
			return JsonResponse(context)

		if settype == "email":

			email = request.POST.get("email").strip().lower()


			if request.user.email == email:
				errors.append("New email can not be same as previous email")
				context["errors"]=errors
				return JsonResponse(context)
			
			else:
				
				if user_exists(email):
					errors.append("Email already taken")
				elif not check_email_dns(email):
					errors.append("Invalid Email")

				if errors:
					context["errors"]=errors
					return JsonResponse(context)


			request.user.email = email
			ud = request.user.userdetails
			res = send_email_confirmation_mail(request.get_host(), ud, request.user.email)
			if not res:
				context["errors"]=["Something went wrong. Please Try Again"]
				return JsonResponse(context)

			request.user.save()


			context["success"] = True
			return JsonResponse(context)


	return JsonResponse(context)


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

		auth_base = request.user.userdetails.auth_base
		if auth_base!=1:
			if auth_base==2:
				context["error"] = "Your account is connected to facebook. You cannot change your password. Use facebook to login"
			
			return JsonResponse(context)

		chk = authenticate(username=request.user.username, password=cpass)

		if not chk:
			context["success"]=False
			errors.append("Wrong old Password")
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


		request.user.set_password(passwd)
		request.user.save()

		new = authenticate(username=request.user.username, password=passwd)
		login(request, new)
		context["success"] = True

		return JsonResponse(context)






def registerContest(request):
	context={"success": False, "auth": True}

	if not request.user.is_authenticated:
		context["error"] = "You are not logged in"
		context["auth"] = False
		return JsonResponse(context)

	if not request.user.userdetails.is_account_confirmed():
		context["error"] = "Your email is not confirmed. Confirm your email to register for contest"
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


	



def auth_mail(request):

	cont = send_auth_mail()
	

	return HttpResponse("result = "+str(cont))
