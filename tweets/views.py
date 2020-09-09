from django.shortcuts import render , redirect
import json
from django.http import HttpResponse , Http404 , JsonResponse
from .models import Tweet
import random
from .forms import TweetForm
from .serializers import TweetSerializer

def home_view(request):
    return render(request , 'pages/home.html' , {})


def tweet_list_view(request):
    qs = Tweet.objects.all()
    data = {"response" : [x.serialize() for x in qs]}
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

def tweet_create(request):
    serializer = TweetSerializer(data = request.POST or None)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return JsonResponse(serializer.data , status=201)
        
    return JsonResponse({} , status=400)


def tweet_create_pure(reqeust):
    if not reqeust.user.is_authenticated:
        if reqeust.is_ajax():
            return JsonResponse({} , status=401)
        return redirect("/login")
    form = TweetForm(reqeust.POST or None)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        tweet = Tweet(content=content)
        tweet.user = reqeust.user
        tweet.save()
        if reqeust.is_ajax():
            return JsonResponse(tweet.serialize() , status=201)
        form = TweetForm()
        if reqeust.POST.get('next' , None) is not None:
            return redirect(reqeust.POST.get('next'))
    if form.errors():
        return JsonResponse(form.errors , status=400)
    return render(reqeust , 'components/forms.html' , context={"form" : form})