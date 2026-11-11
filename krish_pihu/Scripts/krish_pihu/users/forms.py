from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


# 1. Naya User banane ke liye Form (Sign Up)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


# 2. Aapka purana Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'headline', 'bio', 'skills', 'phone', 'location', 'github_link', 'linkedin_link']
