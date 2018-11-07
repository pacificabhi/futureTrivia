from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.trivia.models import Trivia, Question
from .utility import *
from apps.trivia.utility import get_question
from futuretrivia.utility import get_current_time
import json, ast
from time import sleep
# Create your views here.



def communityHome(request):

	return render(request, 'community/communityhome.html', {})


@login_required
def hostedTrivia(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))

	context={}

	hostedtrivias = Trivia.objects.filter(admin=request.user).order_by("-start_time")
	context["hostedtrivias"] = hostedtrivias
	return render(request, 'community/hostedtrivia.html', context)



def editTrivia(request, code):


	#SAVING UPDATED TRIVIA

	if request.method == "POST" and request.is_ajax():
		context = {"success": False}

		if not request.user.is_authenticated:
			context["error"] = "You are not logged in"
			return JsonResponse(context)

		trivia_form = request.POST.get("trivia_form")
		
		if trivia_form:
			trivia_form = json.loads(trivia_form) #converting form json string to python dict
			valid = is_valid_trivia(trivia_form) #utility function to check if trivia is valid, it return a dict {error, form}

			if not valid[0]:
				context["errors"] = valid[1]
				context["success"] = False
				context["form_errors"] = True
				return JsonResponse(context)

			trivia_form = valid[1] #valid trivia_form
			trivia = Trivia.objects.filter(code=code).first()  #getting trivia model object from database

			if trivia:
				if trivia.admin == request.user:
					if trivia.start_time:
						now = get_current_time()
						endtime = trivia.get_endtime()
						
						if endtime<=now:
							context["error"]="You are not allowed to edit %s as it is already ended"%(trivia.code) # trivia already started so not allowed to edit
							context["success"]=False
							return JsonResponse(context)
							
						if trivia.start_time<=now:
							context["error"]="You are not allowed to edit %s as it is already started"%(trivia.code) # trivia already started so not allowed to edit
							context["success"]=False
							return JsonResponse(context)


					trivia.name = trivia_form["name"]
					trivia.password = trivia_form["password"]
					trivia.category = trivia_form["category"]
					trivia.poster = trivia_form["poster"]
					trivia.quote = trivia_form["quote"]
					trivia.prizes = trivia_form["prizes"]
					trivia.about = trivia_form["about"]
					trivia.announcements = trivia_form["announcement"]
					trivia.start_time  = trivia_form["start_time"]
					trivia.duration = trivia_form["duration"]
					trivia.portal_duration = trivia_form["portal_duration"]
					trivia.can_change_answer = trivia_form["can_change_answer"]
					trivia.individual_timing = trivia_form["individual_timing"]
					trivia.private = trivia_form["private"]
					trivia.ready = trivia_form["ready"]
					trivia.set_endtime()


					trivia.save()
					context["success"] = True


				else:
					context["error"]="You are not allowed to edit %s."%(trivia.code) #if request user is not admin of trivia
					context["success"]=False
					return JsonResponse(context)

			else:
				context["error"]="Trivia does not exist." # if there is no trivia with requested code
				context["success"]=False
				return JsonResponse(context)



		return JsonResponse(context)


	elif request.method == "POST":

		return JsonResponse({"success": False, "error": "Request not identified"})

		
	#GET REQUEST EDIT PAGE

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))
	context={"error":"Not found"}

	trivia = Trivia.objects.filter(code=code).first()

	if trivia:

		if trivia.admin == request.user:

			context["trivia"]=trivia
			context["serverdatetime"]=get_current_time()

		else:

			context["error"]="You are not allowed to edit %s."%(trivia.code)

	else:
		context["error"]="Trivia does not exist."


	return render(request, 'community/edittrivia.html', context)





def lockTrivia(request):

	
	context={"success": False}

	if not request.user.is_authenticated:
		context["error"] = "You are not logged in"
		return JsonResponse(context)

	code = request.GET.get("code")
	if not code:
		context["error"] = "Invalid Request"
		return JsonResponse(context)		

	trivia = Trivia.objects.filter(code=code).first()

	if trivia:
		if trivia.admin == request.user:
			if trivia.locked:
				context["error"]="Trivia already locked"
				return JsonResponse(context)

			res = trivia.lock()
			if res:
				context["success"]=True
			else:
				context["error"]="Trivia can not be locked"
				return JsonResponse(context)

	else:
		context["error"] = "Trivia does not exist"
		return JsonResponse(context)		


	return JsonResponse(context)


def hostedTriviaQuestions(request, code):

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))
	context={"error":"Not found"}

	trivia = Trivia.objects.filter(code=code).first()

	if trivia and trivia.admin == request.user:
		#triviaquestions = trivia.question_set.all()
		context["trivia"] = trivia

	else:
		return render(request, 'trivia/not_found.html', {})

	#print("title== ", trivia.question_set.all().first().get_title())

	return render(request, 'community/hostedtriviaquestions.html', context)


def deleteQuestion(request, code):
	context={"success": False}

	q_id = request.GET.get("q_id")
	if q_id:
		q_id = int(q_id)
		ques = Question.objects.filter(id=q_id).first()

		if ques:
			if ques.trivia.code == code and ques.trivia.admin == request.user:
				if not ques.trivia.is_ended() and not ques.trivia.is_started():
					ques.delete()
					context["success"] = True
				
				else:
					context["error"] = "Can not delete this questions as trivia already started or ended"
					return JsonResponse(context)

			else:
				context["error"] = "You are not allowed to delete this question"
				return JsonResponse(context)	

		else:
			context["error"] = "Question does not exist"
			return JsonResponse(context)	

	else:
		context["error"] = "Question id invalid"
		return JsonResponse(context)


	return JsonResponse(context)




@login_required
def editQuestion(request, code): #view to get question or save it

	#post request to save question
	#request.method == "POST" and request.is_ajax()

	if request.method=="POST" and request.is_ajax():
		#print("ajax")
		context = {"new": False, "success": False}

		ques_form = request.POST.get("ques_form")
		#print(ques_form)

		if ques_form:
			#print(ques_form)
			ques_form = json.loads(ques_form)
			q_id = ques_form["id"]
			#print(type(q_id))

			if q_id or q_id==0:
				#q_id = int(q_id)

				form_errors=[]
				positive_score = int(ques_form["positive_score"])
				negative_score = int(ques_form["negative_score"])
				title = ques_form["title"].strip()

				if len(title)<=0:
					form_errors.append("Title can not be blank")
				elif len(title)>40:
					form_errors.append("Title can not contain more than 40 characters");


				if positive_score < 0 or negative_score < 0:
					form_errors.append("Value of scores can not be negative")

				options_dict = ques_form["options"]

				if not options_dict:
					form_errors.append("Question must have options")

				correct_answer = ques_form["correct_answer"]
				correct_answer_chosen = False
				options = {}

				for opt_id in options_dict.keys():
					value = options_dict[opt_id]
					opt_id = int(opt_id)
					options[opt_id] = value

					if opt_id == correct_answer:
						correct_answer_chosen = True

				if not correct_answer_chosen:
					form_errors.append("There must be one correct option")

				if form_errors:
					context["form_errors"] = form_errors
					return JsonResponse(context)



				if q_id!=0:  #edit _question
					q_obj = Question.objects.filter(id=q_id).first()
					if q_obj:
						if q_obj.trivia.code == code and q_obj.trivia.admin == request.user:
							q_obj.question = ques_form["statement"]
							q_obj.explaination = ques_form["explaination"]
							q_obj.options = options
							q_obj.positive_score = positive_score
							q_obj.negative_score = negative_score
							q_obj.correct_answer = correct_answer
							q_obj.title = title
							#print(q_obj.explaination)
							q_obj.save()

							context["success"] = True

						else:
							context["error"] = "You are not authorised to edit this question"
							return JsonResponse(context)


					else:
						context["error"] = "No Question to edit"
						return JsonResponse(context)

				else: #new question
					trivia = Trivia.objects.filter(code=code).first()
					if trivia and trivia.admin == request.user:
						Question.objects.create(title=title, question=ques_form["statement"], explaination=ques_form["explaination"], options=options, positive_score=positive_score, negative_score=negative_score, correct_answer=correct_answer, trivia=trivia)
						context["success"]=True


					else:
						context["error"] = "You are not authorised to add new question"
						return JsonResponse(context)

			else:
				context["error"] = "Invalid action"
				return JsonResponse(context)

		

		else:
			context["error"] = "Invalid action"
			return JsonResponse(context)

		return JsonResponse(context)


	elif request.method=="POST":
		context["error"] = "Invalid action"
		return JsonResponse(context)



		#print("get")

	#GET request to fetch question(if exist)

	context={"success": False}

	q_id = request.GET.get("q_id")
	if q_id:
		q_id = int(q_id)
		q_obj = Question.objects.filter(id=q_id).first()

		if q_obj:
			if q_obj.trivia.admin==request.user and q_obj.trivia.code==code:
				ques=get_question(q_obj)
				ques["explaination"] = q_obj.explaination
				ques["correct_answer"] = q_obj.correct_answer
				ques["duration"] = q_obj.duration
				#ques["title"] = q_obj.get_title()
				context["q_obj"] = ques
				context["success"] = True

			else:
				context["error"] = "Unauthorise Request"
				return JsonResponse(context)


		else:
			context["error"] = "Invalid Request"
			return JsonResponse(context)


	else:
		context["error"] = "Invalid Question"
		return JsonResponse(context)		




	return JsonResponse(context)