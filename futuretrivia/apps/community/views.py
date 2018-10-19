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