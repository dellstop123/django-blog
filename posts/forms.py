from django import forms
from pagedown.widgets import PagedownWidget
from string import Template
from django.utils.safestring import mark_safe
from .models import Post, Images,AddUserProfile
from django.contrib.auth.models import User
from django.forms import widgets
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
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
#     IsStaff = forms.BooleanField(label='IsStaff')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
#             'IsStaff'
        ]

class AddUserProfileForm(forms.ModelForm):
#     bio = forms.CharField()
#     image = forms.ImageField()

    class Meta:
        model = AddUserProfile
        fields = [
            'bio',
            'image',
        ]
        
class PasswordForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'password',
        ]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = [
            'post',
            'image',
        ]


# class PictureWidget(forms.widgets.Widget):
#     def render(self, name, value, attrs=None, **kwargs):
#         html = Template("""<img src="$link"/>""")
#         return mark_safe(html.substitute(link=value))
