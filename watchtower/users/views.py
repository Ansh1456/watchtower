import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import RegisterForm, LoginForm, OTPForm


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            otp = str(random.randint(100000, 999999))
            UserProfile.objects.create(user=user, otp=otp, is_verified=False)
            request.session['pending_user_id'] = user.id
            # In a real app, send email. Here we just show it.
            messages.info(request, f"Demo OTP (simulated): {otp}")
            return redirect('verify_otp')
    return render(request, 'users/register.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('login')

    form = OTPForm()
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            try:
                profile = UserProfile.objects.get(user_id=user_id)
                if profile.otp == entered_otp:
                    profile.is_verified = True
                    profile.save()
                    del request.session['pending_user_id']
                    messages.success(request, "Email verified! Please log in.")
                    return redirect('login')
                else:
                    messages.error(request, "Invalid OTP. Try again.")
            except UserProfile.DoesNotExist:
                messages.error(request, "Something went wrong.")

    return render(request, 'users/verify_otp.html', {'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                try:
                    profile = user.userprofile
                    if not profile.is_verified:
                        messages.warning(request, "Please verify your email first.")
                        request.session['pending_user_id'] = user.id
                        return redirect('verify_otp')
                except UserProfile.DoesNotExist:
                    pass
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials.")
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
