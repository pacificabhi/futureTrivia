from django.shortcuts import render
from .models import Trivia
import pytz, datetime
from django.http import *

# Create your views here.

def triviaGames(request):

	context={}
	now=datetime.datetime.now().replace(tzinfo=pytz.utc)
	trivias=Trivia.objects.filter(private=False).order_by('start_time')
	
	present=[]
	past=[]
	future=[]

	#print(request.user.userdetails.trivias.all())

	#tz=pytz.timezone('Asia/Kolkata')

	for triv in trivias:
		#print(trivia.code)
		#print(triv not in request.user.userdetails.trivias.all(), " ", triv.code)
		trivia = triv
		endtime = triv.start_time + datetime.timedelta(seconds=triv.duration) #finding end time
		portal_endtime = triv.start_time + datetime.timedelta(seconds=triv.portal_duration) #finding registration end time
		
		trivia.duration=trivia.duration//60;
		tr = []
		if now > portal_endtime: #Checking if registration ended
			tr = [trivia, False]
		else:
			tr = [trivia, True]


		if triv.start_time > now: #if contest started and active now
			future.append(tr)
		elif endtime < now:
			past.append(tr)
		else:
			present.append(tr)


		context["trivias"]={"present":present, "past": past, "future": future}



	return render(request, 'trivia/triviaGames.html',context)


def triviaDetails(request, code):
	trivia = Trivia.objects.filter(code=code).first()

	#intialising
	context = {"exist":False, "ended": False, "can_register": False, "can_start": False, "private": True, "authentic": False, "auth_error": False}

	#if request is port for private contest authentication
	if request.method == "POST":
		password = request.POST.get("password")

		if password == trivia.password:
			context["authentic"] = True
		else:
			context["auth_error"]=True
			context["auth_error"] = "Wrong Password"


	if trivia:
		context["private"]=trivia.private
		now = datetime.datetime.now().replace(tzinfo=pytz.utc)

		if (not trivia.private) or context["authentic"]:

			endtime = trivia.start_time + datetime.timedelta(seconds=trivia.duration)
			regendtime = trivia.start_time + datetime.timedelta(seconds=trivia.portal_duration) #getting registration end time
				
			#removing Trailing spaces

			trivia.poster = trivia.poster.strip()
			trivia.name = trivia.name.strip()
			trivia.announcements = trivia.announcements.strip()
			trivia.about = trivia.about.strip()
			trivia.prize = trivia.prize.strip()
			trivia.quote = trivia.quote.strip()
			
			trivia.duration = trivia.duration//60;

			if endtime < now:  #if contest ended
				context["ended"]=True
			else:
				if regendtime > now: # if registration ended
					context["can_register"] = True

				if trivia.start_time < now and endtime > now:  # if contest is active now
					context["can_start"]=True

			context["trivia"] = trivia
			context["endtime"] = endtime

		context["exist"] = True 

	return render(request, 'trivia/triviaDetails.html', context)


def registerContest(request):
	context={"success": False}

	if not request.user.is_authenticated:
		context["error"] = "Sign in to Register"
		return JsonResponse(context)

	code = request.GET.get("code")
	trivia = Trivia.objects.filter(code=code)
	
	if not trivia:
		context["error"] = "Contest Not Found"
		return JsonResponse(context)

	now=datetime.datetime.now().replace(tzinfo=pytz.utc)
	portal_endtime = trivia.start_time + datetime.timedelta(seconds=trivia.portal_duration)

	if now > portal_endtime:
		context["error"] = "Registration ended"
		return JsonResponse

	request.user.userdetails.trivias.add(trivia)
	context["success"] = True

	return JsonResponse(context)
	