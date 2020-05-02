from __future__ import unicode_literals
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
# from django.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
# Create your models here.
from markdown_deux import markdown

from comment.models import Comment

from .utils import get_read_time


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # overriding all() of Post method
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s%s%s" % (instance.id, instance.id, extension)
    return "%s%s" % (instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    # models.TimeField(null=True, blank=True) #assume minutes
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_reciever, sender=Post)


class User(models.Model):
    username = models.CharField(max_length=120)
    email = models.EmailField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    isStaff = models.BooleanField()
    # password = models.CharField(max_length=120)
