from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    form = AuthenticationForm(request.POST or None)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username , password=password)
    if user is not None:
        login(request ,user)
        return redirect(request.GET.get("next" , "/list"))
    return render(request , "accounts/login.html" , {"form" : form})

def logout_view(reqeust):
    logout(reqeust)
    return redirect('/login')

def register_view(request):
    form  = UserCreationForm(request.POST or None)
    if form.is_valid():
        User.objects.create_user(username=form.cleaned_data.get("username") , password=form.cleaned_data.get("password1"))
        return redirect('/login')
    return render(request , "accounts/login.html" , {"form" : form})