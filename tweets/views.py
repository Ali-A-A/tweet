from django.shortcuts import render , redirect
import json
from django.http import HttpResponse , Http404 , JsonResponse
from .models import Tweet
import random
from .forms import TweetForm

def home_view(request):
    return render(request , 'pages/home.html' , {})


def tweet_list_view(request):
    qs = Tweet.objects.all()
    data = {"response" : [{"id" : x.id , "content" : x.content , "likes" : random.randint(1 , 50)} for x in qs]}
    return JsonResponse(data)


def tweet_detail(request , id):

    data = {
        "id" : id,
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=id)
        data['content'] = tweet.content
    except:
        data['message'] = 'Not Found'
        status = 404
        
    
    return JsonResponse(data , status=status)


def tweet_create(reqeust):
    form = TweetForm(reqeust.POST or None)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        tweet = Tweet(content=content)
        tweet.save()
        form = TweetForm()
        if reqeust.POST.get('next' , None) is not None:
            return redirect(reqeust.POST.get('next'))
    return render(reqeust , 'components/forms.html' , context={"form" : form})