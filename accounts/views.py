from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import os
from django.contrib.auth import update_session_auth_hash
from .email import mail
from datetime import timedelta
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.signals import user_logged_in, user_logged_out
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm

SUBJECT = "Thanks For Registration!"
TEXT = "Hi! Welcome to BlogBook.You can create, update and modify your own Blog in this Platform and share this on Facebook Posts."
message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


def login_view(request):
    # print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/posts")
    return render(request, "login.html", {"form": form, "title": title, })


def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        mail(user.email, message)
        messages.success(request, "Please Login again to confirm email",
                         extra_tags='html_safe')
        if next:
            return redirect(next)
        return redirect("/posts")

    context = {
        "form": form,
        "title": title,
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            SUBJECT = "Password Changed"
            TEXT = "Your BlogBook Password has been changed successfully!"
            pwd_message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            mail(user.email, pwd_message)
            return redirect('/posts/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,
        "title": "Change Password"
    })


@login_required
def setting(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() >
                      1 or user.has_usable_password())

    return render(request, 'settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})
