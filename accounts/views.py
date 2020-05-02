from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.shortcuts import render, redirect
from django.contrib import messages
import os
from .email import mail
from .forms import UserLoginForm, UserRegisterForm


SUBJECT = "New Django Blog Developed by Guneet Singh !"
TEXT = "Hi! Welcome to Django Blog"
message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


def login_view(request):
    print(request.user.is_authenticated())
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
    return render(request, "form.html", {"form": form, "title": title})


def register_view(request):
    print(request.user.is_authenticated())
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
        "title": title
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
            TEXT = "Your Django-Blog Password has been changed successfully!"
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
