from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User
from .forms import RegisterForm, LoginForm


def register_view(request):
    # If user somehow lands here while already logged in, send them home
    if request.user.is_authenticated:
        return redirect('citizen_dashboard')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            # Log them in immediately after registering — no extra step
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account is ready.')
            return redirect('citizen_dashboard')
        else:
            # form.errors will be shown in the template automatically
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        # Already logged in — route them to the right portal
        if request.user.role in ['officer', 'admin']:
            return redirect('officer_dashboard')
        return redirect('citizen_dashboard')

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Send officer/admin to their own portal
                if user.role in ['officer', 'admin']:
                    return redirect('officer_dashboard')
                return redirect('citizen_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
