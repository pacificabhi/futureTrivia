from django.shortcuts import render
from .models import *
import pytz, datetime
from django.http import *
from django.utils.safestring import mark_safe
import json, ast
from .utility import *
from django.contrib.auth.decorators import login_required
from django.core import serializers


# Create your views here.

def triviaGames(request):

	context={}
	now=get_current_time()
	trivias=Trivia.objects.filter(private=False).order_by('start_time')
	
	present=[]
	past=[]
	future=[]

	for triv in trivias:
		
		trivia = triv
		endtime = get_endtime(triv) #finding end time
		portal_endtime = endtime #finding registration end time
		
		
		if triv.start_time > now: #if contest started and active now
			future.append(triv)
		elif endtime < now:
			past.append(triv)
		else:
			present.append(triv)


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
		now = get_current_time()

		if (not trivia.private) or context["authentic"]:

			endtime = get_endtime(trivia)
			#regendtime = endtime #getting registration end time
				
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
				# if registration ended
				context["can_register"] = True

				before_start = (int)((trivia.start_time-now).total_seconds())
				before_start -= 120
				context["before_start"]=before_start

				if before_start <= 0 and endtime > now:  # if contest is active now
					context["can_start"]=True
				#print(context["can_start"])

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

	now=get_current_time()
	portal_endtime = get_endtime()

	if now > portal_endtime:
		context["error"] = "Registration ended"
		return JsonResponse


	request.user.userdetails.trivias.add(trivia)
	context["success"] = True

	return JsonResponse(context)




@login_required
def triviaPlay(request, code):

	trivia = Trivia.objects.filter(code=code).first()

	#intialising
	context = {"user_applicable":False, "ended": True, "started_by_user": False}

	if trivia:
		context["user_applicable"]=True

		now = get_current_time()
		endtime = get_endtime(trivia)

		if now<endtime:
			context["ended"] = False
			if trivia in request.user.userdetails.trivias.all():
				started_by_user = bool(TriviaResult.objects.filter(username=request.user, trivia=trivia).count())
				context["started_by_user"] = started_by_user
				if trivia.start_time < now:  # if contest is active now
					context["can_begin"]=True
					context["total_number_of_questions"]=len(trivia.question_set.all())

		context["trivia"]=trivia


	return render(request, 'trivia/triviaplay.html', context)
	

@login_required
def triviaStart(request, code):
	context = {"success": False}
	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code).first()
	if trivia:
		if trivia not in request.user.userdetails.trivias.all():
			context["error"]="You are not registered for this contest."
			context["success"]=False
			return JsonResponse(context)

		result = TriviaResult.objects.filter(username=request.user, trivia=trivia).first()
		now = get_current_time()
		if not result:
			started_at = now
			if not trivia.individual_timing:
				started_at = trivia.start_time

			tr = TriviaResult.objects.create(username=request.user, trivia=trivia, start_time=started_at, modified_at=now)
			context["success"]=False
		else:
			context["success"]=False
			context["already_started"]=True

	else:
		context["error"]="Contest does not exist"
		return JsonResponse(context)

	return JsonResponse(context)


@login_required
def allTriviaQuestions(request, code):
	context={"success":False}
	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code).first()

	if trivia:
		result = TriviaResult.objects.filter(username=request.user, trivia=trivia).first()
		if not result:
			context["error"]="You are not registered for this contest."
			context["success"]=False
			return JsonResponse(context)

		


		questions_objects = trivia.question_set.all()
		all_questions=[]
		for q in questions_objects:
			
			que = get_question(q)
			all_questions.append(que)


		context["success"]=True
		context["questions"]=all_questions


	else:
		context["error"]="Contest does not exist"
		context["success"]=False
		return JsonResponse(context)




	return JsonResponse(context)