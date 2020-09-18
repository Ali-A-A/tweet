from django.shortcuts import render , redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm


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