from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100 , required=False)
    last_name = forms.CharField(max_length=100 , required=False)
    email_name = forms.CharField(max_length=100 , required=False)

    class Meta:
        model = Profile
        fields = ['bio']