from django.shortcuts import render
from django.http import *
from django.urls import reverse


# Create your views here.


def aboutHome(request):

	return HttpResponseRedirect(reverse('codeofconduct'))



def codeOfConduct(request):
	

	return render(request, 'about/codeofconduct.html', {})