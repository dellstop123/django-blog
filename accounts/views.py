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


def login_view(request):
    print(request.user.is_authenticated())
    password = os.getenv('PASSWORD')
    email = os.environ.get('EMAIL')
    print(password, email)
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
        mail(user.email)
        messages.success(request, "Email Sent Successfully",
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
