from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post, Video, Images
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=PagedownWidget(attrs={"show_preview": False}))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    # image = forms.ImageField(label='Image')

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
    IsStaff = forms.BooleanField(label='IsStaff')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'IsStaff'
        ]


class PasswordForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'password',
        ]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["name", "videofile"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ['post', 'image', ]
