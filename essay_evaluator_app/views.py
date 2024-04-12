from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import requests
from openai import OpenAI
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import EssayTable
from django.utils import timezone
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Create your views here.

def spelling_errors_response(topicinput, contentinput):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, that only replies in number"},
            {"role": "user", "content": f"Title: {topicinput}\nEssay Content: {contentinput}\n How many spelling errors are there? reply in between 0 to 500 in integer\n"},
        ]
    )
    answer = response.choices[0].message.content
    return answer

def content_relevance_response(topicinput, contentinput):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, that only replies in one word"},
            {"role": "user", "content": f"Title: {topicinput}\nEssay Content: {contentinput}\nIs the content relevant to the title? reply with only True or False in text\n"},
        ]
    )
    answer = response.choices[0].message.content
    return answer

def rating_response(topicinput, contentinput):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, that only replies in number"},
            {"role": "user", "content": f"Title: {topicinput}\nEssay Content: {contentinput}\nRate the essay out of 10: reply in between 0 to 10 in integer only:\n"},
        ]
    )
    answer = response.choices[0].message.content
    return answer
    

def home(request):
    if request.user.is_authenticated:
        past_searches = EssayTable.objects.filter(user = request.user).order_by('-time')
    
    if request.method == 'POST':
        topicinput = request.POST.get('topicinput')
        contentinput = request.POST.get('contentinput')
        spelling_errors = spelling_errors_response(topicinput,contentinput)
        content_relevance = content_relevance_response(topicinput,contentinput)
        rating = rating_response(topicinput,contentinput)
        
        if request.user.is_authenticated:
            feedback = EssayTable(user = request.user, title = topicinput, content = contentinput, spelling_errors = spelling_errors, relevant_content = content_relevance, score = rating, time = timezone.localtime(timezone.now()))
            feedback.save()
            
        return JsonResponse({'topicinput': topicinput, 'contentinput': contentinput, 'spelling_errors' : spelling_errors, 'content_relevance' : content_relevance, 'rating' : rating})
    
    if request.user.is_authenticated and len(past_searches) > 0:
        return render(request, 'essay_evaluator_app/home.html', {'past_searches' : past_searches})
    else:
        return render(request, 'essay_evaluator_app/home.html')

def login(request):
    return render(request, 'essay_evaluator_app/login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')
