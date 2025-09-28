from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserLoginForm, CustomUserCreationForm
from django.db import IntegrityError
from django.contrib.auth import logout as auth_logout
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # AuthenticationForm already authenticated the credentials; get_user() returns the user
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                # Race condition: email uniqueness enforced at DB level
                form.add_error('email', 'A user with that email already exists.')
            else:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')