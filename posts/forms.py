from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]


class ProfileForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
