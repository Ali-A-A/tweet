from django.shortcuts import render , redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
import json


User = get_user_model()


def profile_updata_view(request):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profiles/update")
    my_profile = request.user.profile
    next = ""
    form = ProfileForm(request.POST or None , instance=my_profile)
    if form.is_valid():
        user = request.user
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email_name = form.cleaned_data.get("email_name")
        user.first_name = first_name
        user.last_name = last_name
        user.email = email_name
        user.save()
        profile_obj.save()
        return redirect("/list")
    context = {
        "form" : form
    }
    return render(request , "accounts/login.html" , context)

@login_required(login_url="/login")
def profile_view(reqeust):
    qs = Profile.objects.filter(user__username=reqeust.user.username)
    if not qs.exists():
        raise Http404("Profile Not Found")
    context = {
        "profile_username" : reqeust.user.username,
        "profile" : qs.first()
    }
    return render(reqeust , "profiles/detail.html" , context)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_follow(request , username):
    curr_user = request.user
    to_follow_qs = User.objects.filter(username=username)
    if not to_follow_qs.exists():
        return Response({} , status=404)
    to_follow = to_follow_qs.first()
    profile = to_follow.profile
    if curr_user.username == username:
        return Response({"count" : profile.followers.all().count()} , status=200)
    data = {}
    try:
        data = request.data 
    except:
        pass
    action = data.get("action")
    if action == "follow":
        profile.followers.add(curr_user)
    elif action == "unfollow":
        profile.followers.remove(curr_user)
    return Response({"count" : profile.followers.all().count()} , status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request , *args , **kwargs):
    panigator = PageNumberPagination()
    panigator.page_size = 20
    user = request.user
    profiles = user.following.all()
    followed_users_id = []
    if profiles.exists():
        followed_users_id = [x.user.id for x in profiles]
    followed_users_id.append(user.id)
    qs = Tweet.objects.filter(user__id__in=followed_users_id)
    panigator_qs = panigator.paginate_queryset(qs , request)
    serializer = TweetSerializer(panigator_qs , many=True)
    return panigator.get_paginated_response(serializer.data)