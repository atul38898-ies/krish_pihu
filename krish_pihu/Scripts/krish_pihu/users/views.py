from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import ProfileUpdateForm, UserRegisterForm
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # User ko automatically login karein
            messages.success(request, f'Account created for {user.username}! Apni profile details bharein.')
            return redirect('edit_profile')  # Seedha profile edit page par bhejein
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def view_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    skills_list = [skill.strip() for skill in profile.skills.split(',')] if profile.skills else []
    return render(request, 'view_profile.html', {
        'profile': profile,
        'skills_list': skills_list
    })


def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    skills_list = [skill.strip() for skill in profile_user.userprofile.skills.split(',')] if profile_user.userprofile.skills else []
    return render(request, 'view_profile.html', {
        'profile': profile_user.userprofile,
        'skills_list': skills_list
    })


def download_vcard(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.userprofile
    
    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
N:{user.last_name};{user.first_name};;;
FN:{user.first_name} {user.last_name}
TITLE:{profile.headline}
TEL;TYPE=CELL:{profile.phone}
EMAIL:{user.email}
URL:{request.build_absolute_uri(f'/profile/{user.username}/')}
NOTE:{profile.bio}
END:VCARD"""

    response = HttpResponse(vcard_content, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{user.username}.vcf"'
    return response
