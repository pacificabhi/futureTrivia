from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.trivia.models import Trivia
from .utility import *
from futuretrivia.utility import get_current_time
import json
# Create your views here.


def communityHome(request):
	return HttpResponseRedirect(reverse('hostedtrivia'))


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
						if trivia.start_time<=now:
							context["error"]="You are not allowed to edit %s as it is already started"%(trivia.code) # trivia already started so not allowed to edit
							context["success"]=False
							return JsonResponse(context)

						endtime = trivia.get_endtime()
						if endtime<=now:
							context["error"]="You are not allowed to edit %s as it is already ended"%(trivia.code) # trivia already started so not allowed to edit
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