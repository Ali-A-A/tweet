from django.shortcuts import render
from django.http import Http404

from .models import Profile

def profile_view(reqeust , username):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        raise Http404("Profile Not Found")
    context = {
        "profile_username" : username,
        "bio" : qs.first().bio
    }
    return render(reqeust , "profiles/detail.html" , context)