from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.trivia.models import Trivia

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


@login_required
def editTrivia(request, code):

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('userlogin'))

	context={}

	return render(request, 'community/edittrivia.html', context)