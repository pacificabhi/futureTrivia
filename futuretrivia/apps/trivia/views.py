from django.shortcuts import render
from .models import *
import pytz, datetime
from django.http import *
from django.utils.safestring import mark_safe
import json, ast
from django.contrib.auth.decorators import login_required
from django.core import serializers
from time import sleep
from math import ceil
from .utility import *
from futuretrivia.utility import *


# Create your views here.

def triviaGames(request):

	context={}
	now=get_current_time()
	trivias=Trivia.objects.filter(private=False, ready=True).order_by('start_time')
	
	present=[]
	past=[]
	future=[]

	for triv in trivias:
		
		trivia = triv
		endtime = triv.get_endtime() #finding end time
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


	if trivia and trivia.ready:
		context["private"]=trivia.private
		now = get_current_time()

		if (not trivia.private) or context["authentic"]:

			#endtime = trivia.get_endtime()
			#regendtime = endtime #getting registration end time
				
			#removing Trailing spaces

			trivia.poster = trivia.poster.strip()
			trivia.name = trivia.name.strip()
			trivia.announcements = trivia.announcements.strip()
			trivia.about = trivia.about.strip()
			trivia.prizes = trivia.prizes.strip()
			trivia.quote = trivia.quote.strip()
			


			if trivia.is_fully_ended():  #if contest ended
				context["ended"]=True

			else:
				# if registration ended
				context["can_register"] = True

				before_start = (int)((trivia.start_time-now).total_seconds())
				before_start -= 120
				context["before_start"]=before_start

				if before_start <= 0 and not trivia.is_ended():  # if contest is active now
					context["can_start"]=True
				#print(context["can_start"])

			context["trivia"] = trivia
			#context["endtime"] = endtime

		context["exist"] = True 

	else:
		return render(request, 'trivia/not_found.html', {})

	return render(request, 'trivia/triviaDetails.html', context)



"""
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
	portal_endtime = trivia.get_endtime()

	if now > portal_endtime:
		context["error"] = "Registration ended"
		return JsonResponse


	request.user.userdetails.trivias.add(trivia)
	context["success"] = True

	return JsonResponse(context)
"""



@login_required
def triviaPlay(request, code):

	trivia = Trivia.objects.filter(code=code).first()

	#intialising
	context = {"user_applicable":False, "ended": False, "started_by_user": False, "user_ended": False}

	if trivia and trivia.ready:
		context["user_applicable"]=True

		now = get_current_time()
		endtime = trivia.get_endtime()
		if now>=endtime:
			context["ended"]=True

		result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
		if result:
			context["started_by_user"] = True
			time_elapsed = int((now-result.start_time).total_seconds())
			if time_elapsed>trivia.duration or submitted(result):
				context["user_ended"] = True

				if result.stars>0:
					context["feedback"]=True

		if trivia in request.user.userdetails.trivias.all():
			if now<endtime:
				context["ended"] = False
				
				if trivia.start_time<now:  # if contest is active now
					context["can_begin"]=True
					context["total_number_of_questions"]=trivia.question_set.all().count()

		context["trivia"]=trivia

		#print("user_ended == ", context["user_ended"])

	else:
		return render(request, 'trivia/not_found.html', {})


	return render(request, 'trivia/triviaplay.html', context)
	


def triviaStart(request, code):
	context = {"success": False}
	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code).first()
	if trivia:
		if trivia not in request.user.userdetails.trivias.all():
			context["error"]="You are not registered for this trivia."
			context["success"]=False
			return JsonResponse(context)

		result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
		now = get_current_time()

		if trivia.start_time>=now:
			context["error"]="Trivia is not started yet"
			context["success"]=False
			return JsonResponse(context)

		if not result:
			started_at = now
			if not trivia.individual_timing:
				started_at = trivia.start_time

			tr = TriviaResult.objects.create(user=request.user, trivia=trivia, start_time=started_at, modified_at=now)
			context["success"]=True
		else:
			context["success"]=True
			context["already_started"]=True

	else:
		context["error"]="Contest does not exist"
		return JsonResponse(context)

	return JsonResponse(context)



def allTriviaQuestions(request, code):

	
	context={"success":False}
	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code).first()

	if trivia:
		result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
		if not result:
			context["error"]="You are not registered for this contest or contest not started"
			context["success"]=False
			return JsonResponse(context)

		time_elapsed = None

		now = get_current_time()
		if trivia.individual_timing:
			time_elapsed = int((now-result.start_time).total_seconds())
		else:
			time_elapsed = int((now-trivia.start_time).total_seconds())

		context["time_left"]=trivia.duration-time_elapsed

		if time_elapsed>trivia.duration or submitted(result):
			context["ended"]=True
			context["error"]="Contest Ended for you"
			context["success"]=False
			return JsonResponse(context)



		questions_objects = trivia.question_set.all()
		all_questions=[]

		extra={"can_change_answer": trivia.can_change_answer, "temp_opt_id":0}

		for q in questions_objects:
			
			que = get_question(q)
			status = get_answer_status(q,result.answers)
			q_obj = {"question":que, "status":status, "extra": extra}
			all_questions.append(q_obj)


		context["success"]=True
		context["questions"]=all_questions


	else:
		context["error"]="Contest does not exist"
		context["success"]=False
		return JsonResponse(context)



	return JsonResponse(context)


def submitAnswer(request, code):
	context={"success": False}

	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)


	if request.method == "POST":
		trivia = Trivia.objects.filter(code=code).first()
		if trivia and not trivia.locked:
			result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
			if result:
				time_elapsed_for_contest = None

				now = get_current_time()
				if trivia.individual_timing:
					time_elapsed_for_contest = int((now-result.start_time).total_seconds())
				else:
					time_elapsed_for_contest = int((now-trivia.start_time).total_seconds())


				if time_elapsed_for_contest<trivia.duration and not submitted(result):
					q_id = int(request.POST.get("q_id"))
					opt_id = int(request.POST.get("opt_id"))
					q_ind = int(request.POST.get("q_ind"))
					time_elapsed = int(request.POST.get("time_elapsed"))
					answers = result.answers
					answers = ast.literal_eval(answers)
					
					if q_id in answers.keys():
						answer = answers[q_id]
						if answer["opt_id"]==0 and answer["time_elapsed"]<=time_elapsed:
							answer["opt_id"]=opt_id
							answer["time_elapsed"]=time_elapsed
							context["success"]=True
							
						elif trivia.can_change_answer and answer["time_elapsed"]<=time_elapsed:
							answer["opt_id"]=opt_id
							answer["time_elapsed"]=time_elapsed
							context["success"]=True

						else:
							context["error"]="Can not change answer"
							
						answers[q_id] = answer


					else:
						answer = {"opt_id": opt_id, "time_elapsed": time_elapsed}
						answers[q_id] = answer
						context["success"]=True

					context["opt_id"]=answers[q_id]["opt_id"]
					context["q_ind"]=q_ind
					answers = str(answers)
					result.answers = answers
					result.save()
					

				else:
					context["contest_ended"]=True
					context["error"]="Contest ended for you"
					return JsonResponse(context)

			else:
				context["error"] = "You are not in contest"
				return JsonResponse(context)
		else:
			context["error"] = "Contest does not exist"
			return JsonResponse(context)
		

	return JsonResponse(context)


def endTest(request, code):
	context={"success": False}


	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)


	if request.method == "POST":
		trivia = Trivia.objects.filter(code=code).first()
		if trivia and not trivia.locked:
			result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
			if result:
				time_taken = None

				now = get_current_time()
				if trivia.individual_timing:
					time_taken = int((now-result.start_time).total_seconds())
				else:
					time_taken = int((now-trivia.start_time).total_seconds())

				if time_taken>trivia.duration:
					time_taken=trivia.duration

				result.calculate_score(questions_set=trivia.question_set.all())
				result.time_taken = time_taken
				result.save()

				context["success"] = True


			else:
				context["error"] = "You are not in contest"
				return JsonResponse(context)
		else:
			context["error"] = "Contest does not exist"
			return JsonResponse(context)




	return JsonResponse(context)



def triviaStars(request, code):
	
	context = {"success": False}

	if not request.user.is_authenticated:
		context["error"] = "You are not logged in"
		return JsonResponse(context)


	trivia = Trivia.objects.filter(code=code).first()
	if not trivia:
		context["error"] = "Trivia does not exist"
		return JsonResponse(context)

	result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
	if not result:
		context["error"] = "You did not participate in %s (%s)"%(trivia.name, trivia.code)
		return JsonResponse(context)

	if result.stars>0:
		context["error"] = "You already rated %s (%s)"%(trivia.name, trivia.code)
		return JsonResponse(context)

	stars = request.GET.get("stars")

	if stars:
		stars=int(stars)
		if stars>0 and stars<=5:
			result.stars=stars
			stars_list  = list(map(int, trivia.stars.strip().split(',')))
			stars_list[stars-1]+=1
			trivia.stars = ",".join(list(map(str, stars_list)))
			trivia.save()
			result.save()
			context["success"] = True

		else:
			context["error"] = "You can only give stars from 1 to 5"

	else:
		context = "Invalid Stars"


	return JsonResponse(context)


def triviaLeaderboard(request, code):
	context={}
	trivia = Trivia.objects.filter(code=code).first()

	if trivia:
		if trivia.private:
			if trivia not in request.user.userdetails.trivias.all():
				return render(request, 'trivia/not_found.html')

		context["trivia"]=trivia

	else:
		return render(request, 'trivia/not_found.html', {})


	return render(request, 'trivia/trivialeaderboard.html', context)


def getRankers(request, code):
	#sleep(10)
	context={"success": False}
	trivia = Trivia.objects.filter(code=code).first()

	if trivia:
		if trivia.private:
			if trivia not in request.user.userdetails.trivias.all():
				context["error"]="Contest not found"
				return JsonResponse(context)

		if not trivia.is_started():
			context["error"]="Contest not started yet"
			return JsonResponse(context)


		rankers_length=20
		page = request.GET.get("page")
		if not page:
			page=1
		else:
			page=int(page)

		if page <= 0:
			page=1

		total_ranks = None
		user_rank = None
		rankers_queryset = None
		start_rank = rankers_length*(page-1)
		result=None

		if request.user.is_authenticated:
			result = TriviaResult.objects.filter(user=request.user, trivia=trivia).first()
		
		if result:
			ranks_set = trivia.triviaresult_set.extra(select={'total_score':'positive_score - negative_score'}, order_by=('-total_score', 'time_taken'))
			total_ranks=len(ranks_set)
			rankers_queryset = ranks_set[start_rank:start_rank+rankers_length]

			for i in range(total_ranks):
				if ranks_set[i] == result:
					user_rank = i+1
					break
			user_record = {"rank": user_rank, "score": result.get_score(), "timing": result.time_taken, "username": result.user.get_username()}
			context["user_record"] = user_record

		else:
			rankers_queryset = trivia.triviaresult_set.extra(select={'total_score':'positive_score - negative_score'}, order_by=('-total_score', 'time_taken'))[start_rank:start_rank+rankers_length]
			total_ranks = trivia.triviaresult_set.all().count()



		rankers=[]
		for ranker in rankers_queryset:
			rank=[ranker.user.get_username(), ranker.user.get_full_name(), ranker.total_score, ranker.time_taken]
			rankers.append(rank)

		context["start_rank"]=start_rank+1
		context["rankers"]=rankers
		context["total_pages"]=ceil(total_ranks/rankers_length)
		context["success"]=True
		

	else:
		context["error"]="No contest found"
		return JsonResponse(context)

	return JsonResponse(context)


def afterAnswer(request, code):


	trivia = Trivia.objects.filter(code=code).first()

	if not trivia:
		return render(request, 'trivia/not_found.html', {})

	context={"trivia":trivia}

	action = request.GET.get("action")

	if not action or action=="page":

		result = TriviaResult.objects.filter(trivia=trivia, user=request.user).first()

		if result:
			context["yes_user"]=True

		return render(request, 'trivia/answers.html', {"trivia": trivia})

	context = {"success": False}

	if not trivia.is_fully_ended():
		context["error"] = "Solutions will be available once trivia ends"
		return JsonResponse(context)

	if action == "answer":
		q_id = request.GET.get("q_id")
		if q_id:
			q_id = int(q_id)
			q_obj = Question.objects.filter(id=q_id).first()

			if q_obj:
				ques=get_question(q_obj)
				ques["explaination"] = q_obj.explaination
				ques["correct_answer"] = q_obj.correct_answer
				ques["duration"] = q_obj.duration
				#ques["title"] = q_obj.get_title()
				context["q_obj"] = ques
				context["success"] = True


			else:
				context["error"] = "No Question found"
				return JsonResponse(context)

		else:
			context["error"] = "No Question found"
			return JsonResponse(context)

	else:
		context["error"] = "Invalid Action"


	return JsonResponse(context)




def userAnswer(request, code):

	context = {"success": False}

	if not request.user.is_authenticated:
		context["error"] = "You are not logged in"
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code).first()

	print("You did not participated in %s"%(trivia.name))
	
	if not trivia:
		context["error"] = "Invalid Request"
		return JsonResponse(context)

	result = TriviaResult.objects.filter(trivia=trivia, user=request.user).first()

	if not result:
		context["error"] = "You did not participated in '%s'"%(trivia.name)
		return JsonResponse(context)


	context["answers"]=ast.literal_eval(result.answers)
	context["success"] = True

	return JsonResponse(context)

