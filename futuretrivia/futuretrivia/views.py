from django.shortcuts import render
from django.http import *
from django.urls import reverse
from apps.trivia.models import Trivia
from .utility import *


# Create your views here.


def index(request):

	context={}

	now = get_current_time()
	trivia = Trivia.objects.filter(start_time__gt=now).order_by("start_time").first()
	if trivia:
		context["time_left"]=trivia.time_to_start()
		context["next_name"]=trivia.name
		context["next_code"]=trivia.code

	#print(trivia)

	if False:
		return HttpResponseRedirect(reverse('triviahome'))

	return render(request, 'trivia/index.html', context)


def notFound(request, url):

	return render(request, 'trivia/not_found.html', {})
