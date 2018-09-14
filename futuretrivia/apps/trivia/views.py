from django.shortcuts import render

# Create your views here.

def triviaGames(request):
	return render(request, 'trivia/triviaGames.html', {})
	