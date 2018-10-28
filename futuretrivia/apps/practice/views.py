from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.trivia.models import Trivia, Question
from django.http import *
from .models import PracticeResult
from futuretrivia.utility import *
from apps.trivia.utility import get_answer_status


# Create your views here.

def practiceHome(request):

	trivias = Trivia.objects.filter(locked=True, ready=True, private=False)
	context={"trivias": trivias}

	return render(request, 'practice/practicehome.html', context)



@login_required
def practicePlay(request):

	context={}
	code=request.GET.get("code")

	if not code:
		return render(request, 'trivia/not_found.html')

	trivia = Trivia.objects.filter(code=code, locked=True, private=False, ready=True).first()

	if not trivia or not trivia.locked:
		return render(request, 'trivia/not_found.html')

	context["trivia"]=trivia

	result = PracticeResult.objects.filter(trivia=trivia, user=request.user, time_taken=0).count()
	if result>0:

		return render(request, 'practice/practiceplay.html', context)


	return render(request, 'practice/instructions.html', context)




def practiceStart(request):

	context={"success": False}

	if not request.user.is_authenticated:
		context["error"] = "You are not logged in"
		return JsonResponse(context)

	code = request.GET.get("code")
	if not code:
		context["error"] = "Trivia does not exist"
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code, locked=True, private=False, ready=True).first()
	if not trivia:
		context["error"] = "Trivia does not exist"
		return JsonResponse(context)

	result = PracticeResult.objects.filter(trivia=trivia, user=request.user, time_taken=0).count()

	if result>0:
		context["already"]=True
		context["success"]=True

	else:
		now = get_current_time()
		tr = PracticeResult.objects.create(user=request.user, trivia=trivia, start_time=now, modified_at=now)
		context["success"]=True

	return JsonResponse(context)



def allPracticeQuestion(request):

	context={"success":False}
	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		return JsonResponse(context)

	code = request.GET.get("code")
	if not code:
		context["error"] = "Trivia does not exist"
		return JsonResponse(context)

	trivia = Trivia.objects.filter(code=code, locked=True, private=False, ready=True).first()
	if not trivia:
		context["error"] = "Trivia does not exist"
		return JsonResponse(context)


	result = PracticeResult.objects.filter(user=request.user, trivia=trivia, time_taken=0).first()
	if not result:
		context["error"]="You did not started this contest for practice"
		context["success"]=False
		return JsonResponse(context)

	time_elapsed = None

	now = get_current_time()
	time_elapsed = int((now-result.start_time).total_seconds())
	


	if time_elapsed>trivia.duration or result.submitted():
		context["ended"]=True
		context["error"]="Practice trivia ended"
		return JsonResponse(context)

	context["time_left"]=trivia.duration-time_elapsed

	questions_objects = trivia.question_set.all()
	all_questions=[]

	extra={"can_change_answer": trivia.can_change_answer, "temp_opt_id":0}

	for q in questions_objects:
		
		que = q.get_question()
		status = get_answer_status(q,result.answers)
		q_obj = {"question":que, "status":status, "extra": extra}
		all_questions.append(q_obj)


	context["success"]=True
	context["questions"]=all_questions

	return JsonResponse(context)




def submitPracticeAnswer(request):
	context={"success": False}

	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)


	if request.method == "POST":

		code = request.POST.get("code")
		if not code:
			context["error"] = "Trivia does not exist"
			return JsonResponse(context)

		trivia = Trivia.objects.filter(code=code, locked=True, private=False, ready=True).first()
		if trivia:

			result = PracticeResult.objects.filter(user=request.user, trivia=trivia, time_taken=0).first()
			if result:

				time_elapsed_for_contest = None

				now = get_current_time()
				
				time_elapsed_for_contest = int((now-result.start_time).total_seconds())


				if time_elapsed_for_contest<trivia.duration and not result.submitted():
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
					context["ended"]=True
					context["error"]="Practice ended for you"
					return JsonResponse(context)

			else:
				context["error"] = "You did not started this trivia for practice"
				return JsonResponse(context)
		else:
			context["error"] = "Trivia does not exist"
			return JsonResponse(context)
		

	return JsonResponse(context)


def endPracticeTest(request):
	context={"success": False}


	if not request.user.is_authenticated:
		context["error"]="You are not logged in"
		context["success"]=False
		return JsonResponse(context)


	if request.method == "POST":

		code = request.POST.get("code")
		print(code)
		if not code:
			print("Not Code")
			context["error"] = "Trivia does not exist"
			return JsonResponse(context)


		trivia = Trivia.objects.filter(code=code, locked=True, private=False, ready=True).first()
		if trivia:
			result = PracticeResult.objects.filter(user=request.user, trivia=trivia, time_taken=0).first()
			if result:
				time_taken = None

				now = get_current_time()

				time_taken = int((now-result.start_time).total_seconds())

				if time_taken>trivia.duration:
					time_taken=trivia.duration

				result.calculate_score()
				result.time_taken = time_taken
				result.save()
				context["result"] = {"score": result.get_score(), "time_taken": result.get_timetaken_string()}

				context["success"] = True


			else:
				context["error"] = "You are not in contest"
				return JsonResponse(context)
		else:
			context["error"] = "Trivia does not exist"
			return JsonResponse(context)




	return JsonResponse(context)


def practiceResult(request):

	pass