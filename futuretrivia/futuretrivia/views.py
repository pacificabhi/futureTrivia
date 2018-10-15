from django.shortcuts import render
from django.http import *
from django.urls import reverse


# Create your views here.


def index(request):

	if True:
		return HttpResponseRedirect(reverse('triviahome'))

	return HttpResponse("<h1>Future Index</h1>")
