from django.shortcuts import render , redirect
import json
from django.http import HttpResponse , Http404 , JsonResponse
from .models import Tweet
import random
from .forms import TweetForm
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .serializers import TweetSerializer , TweetActionSerializer , TweetCreateSerializer
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request , 'pages/home.html' , {})

def tweets_list_view(request):
    return render(request , 'tweets/list.html' , {})

def tweets_detail_view(request , tweet_id):
    print('ddddddddddddddddd' , tweet_id)
    return render(request , 'tweets/detail.html' , {"tweet_id" : tweet_id})

def tweets_profile_view(request , username):
    return render(request , 'tweets/profile.html' , {"profile_username" : username})


def tweet_list_view_pure(request):
    qs = Tweet.objects.all()
    data = {"response" : [x.serialize() for x in qs]}
    return JsonResponse(data)


def tweet_detail_pure(request , id):

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

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create(request):
    serializer = TweetCreateSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data , status=201)
        
    return Response({} , status=400)

@api_view(['GET'])
def tweet_list_view(request):
    qs = Tweet.objects.all()
    username = request.GET.get("username")
    if username is not None:
        qs = qs.filter(user__username__iexact=username)
    serializer = TweetSerializer(qs , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail(request , id):
    obj = Tweet.objects.filter(id=id)
    if not obj.exists():
        return Response({} , status=404)

    serializer = TweetSerializer(obj[0])
    return Response(serializer.data)

@api_view(['DELETE' , 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete(request , id):
    obj = Tweet.objects.filter(id=id)
    if not obj.exists():
        return Response({} , status=404)

    qs = obj.filter(user=request.user)
    if not qs.exists():
        return Response({"message" : "You don't have permission!"} , status=403)
    x = obj[0]
    x.delete()
    return Response({"message" : "Tweet Deleted Successfully"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action(request):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        objs = Tweet.objects.filter(id=id)
        if not objs.exists():
            return Response({} , status=404)
        object = objs.first()
        if action == "like":
            object.likes.add(request.user)
            serializer = TweetSerializer(object)
            return Response(serializer.data)
        elif action == "unlike":
            object.likes.remove(request.user)
            serializer = TweetSerializer(object)
            return Response(serializer.data)
        elif action == "retweet":
            parent = object
            new = Tweet.objects.create(user=request.user , parent=parent , content=content)
            serializer = TweetSerializer(new)
            return Response(serializer.data , status=201)


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