from urllib.parse import quote_plus
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, User
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm, ProfileForm, PasswordForm
from django.db.models import Q
from accounts.views import login_view, logout_view
from comment.forms import CommentForm
from comment.models import Comment

# Create your views here.


def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "post_detail.html", context)


def posts_list(request, id=None):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    title_list = Post.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "Django Blog",
        "page_request_var": page_request_var,
        "today": today,
        "title_list": title_list,

    }
    return render(request, "post_list.html", context)


def posts_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Updated",
                         extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def posts_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")


def about(request):
    # messages.success(request, "Contact Me : +91-7006777505")
    return render(request, "about.html")


def contact(request):
    messages.success(request, "Contact Me : +91-7006777505")
    return render(request, "about.html")


def get_user_profile(request):
    instance = User.objects.get(pk=request.user.id)
    form = ProfileForm(request.POST or None,
                       request.FILES or None, instance=instance)
    if form.is_valid():
        data = form.save(commit=False)
        data.user = request.user
        data.save()
        messages.success(request, "Successfully Updated",
                         extra_tags='html_safe')
        return HttpResponseRedirect('/profile/')
    context = {
        "title": "Update Profile",
        "form": form,
        "instance": instance,
    }
    return render(request, "form.html", context)


def change_pwd(request):
    instance = User.objects.get(pk=request.user.id)
    form = PasswordForm(request.POST or None,
                        request.FILES or None, instance=instance)
    print(instance)
    if form.is_valid():
        data = form.save(commit=False)
        data.user = request.user
        print(data)
        data.save()
        messages.success(request, "Password Changed Successfully",
                         extra_tags='html_safe')
        return logout_view(request)
    context = {
        "title": "Change Password",
        "form": form,
        "instance": instance,
    }
    return render(request, "form.html", context)
