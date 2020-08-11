from urllib.parse import quote_plus
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, User, Preference, Images
from .admin import PostModelAdmin
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm, ProfileForm, PasswordForm, ImageForm
from django.db.models import Q
from accounts.views import login_view, logout_view
from comment.forms import CommentForm
from comment.models import Comment
from django.forms import modelformset_factory
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from newsapi import NewsApiClient
# Create your views here.


def index(request):
    if request.method == 'GET':
        search = request.GET.get('news_search')
    newsapi = NewsApiClient(api_key='494715a553904bed82706d32450566a8')
    top = newsapi.get_top_headlines(sources=search)

    l = top['articles']
    desc = []
    news = []
    img = []
    url = []
    date = []
    name = []
    for i in range(len(l)):
        f = l[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        url.append(f['url'])
        # date.append(f['publishedAt'])

    mylist = zip(news, desc, img, url)

    return render(request, 'news.html', context={"mylist": mylist})





def post_image(request, slug=None):
    imageForm = ImageForm(request.POST or None, request.FILES or None)
    # imageForm = get_object_or_404(Images, slug=slug)
    if imageForm.is_valid():
        image = imageForm.save(commit=False)
        image.user = request.user
        image.save()
        messages.success(request, "Successfully Created")
        # return redirect("posts:mul-images")
        return HttpResponseRedirect(request.path)
    else:
        imageForm = ImageForm()
    context = {
        "imageform": imageForm,

    }
    return render(request, "image/post_image.html", context)


def posts_create(request):
    # if not request.user.is_authenticated():
    #     raise Http404
    # Imageformset = modelformset_factory(
    #     Images, fields=('post', 'image',), extra=1)
    if request.method == 'POST':

        form = PostForm(request.POST or None, request.FILES or None)
        # formset = Imageformset(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.user = request.user

            instance.save()
            value = True
            messages.success(request, "Successfully Created")
            # return redirect("post_list.html")
            return HttpResponseRedirect(instance.get_absolute_url())
            # for f in formset:
            #     try:
            #         photo = Images(
            #             post=instance, image=f.cleaned_data['image'])
            #         photo.save()
            #         messages.success(request, "Successfully Created")
            #         return HttpResponseRedirect(instance.get_absolute_url())
            #     except Exception as e:
            #         break
            # messages.success(request, "Successfully Created")
            # return redirect("post_list.html")
            # message success

    else:
        form = PostForm()
        value = False
        imageForm = ImageForm()
        # formset = Imageformset(queryset=Images.objects.none())
        # print(imageForm.count())
    context = {
        "form": form,
        "value": value,
        "imageform": imageForm,

    }
    return render(request, "post_form.html", context)


def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    post_id = instance.pk
    image = Images.objects.filter(post=post_id)
    count = Images.objects.filter(post=post_id).count()
    count1 = Post.objects.filter(image=instance.image).count()
    total_count = count + 1
    print(total_count)
    print(instance.likes)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
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
    liked = False
    if request.session.get('has_liked_' + str(post_id), liked):
        liked = True
        print("liked {}_{}".format(liked, post_id))
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
        "liked": liked,
        "image": image,
        "count": range(0, total_count),
    }
    return render(request, "post_detail.html", context)


def posts_list(request, id=None):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    title_list = Post.objects.all()
    # image = Post.objects.raw(
    #     """select image,id from posts_post union select image,post_id from posts_images;""")
    # count1 = len(list(image))
    # img = Images.objects.select_related('post')
    # total_count = count1
    # print("<------------->")
    # print(total_count)

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
        "title": "Blog Book",
        "page_request_var": page_request_var,
        "today": today,
        "title_list": title_list,
        # "image": image,
        # "zip": zip(queryset, image),
        # "count": list(image),
        # "img": img,

    }
    return render(request, "post_list.html", context)


def posts_update(request, slug=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
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
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")


def delete_image(request, id=None, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    del_image = Images.objects.get(id=id).delete()
    # del_image.delete()
    return redirect("posts:list")

    # post_id = instance.pk
    # image = Images.objects.filter(post=post_id, is_deleted=1)
    # context = {
    #     "image": image,
    # }
    # return redirect("posts:list")


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


@login_required
def postpreference(request, postid, userpreference):
    if request.method == "POST":
        eachpost = get_object_or_404(Post, id=postid)
        obj = ''
        valueobj = ''
        try:
            obj = Preference.objects.get(user=request.user, post=eachpost)
            valueobj = obj.value  # value of userpreference
            valueobj = int(valueobj)
            userpreference = int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.post = eachpost
                upref.value = userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    eachpost.dislikes += 1
                    eachpost.likes -= 1
                upref.save()
                eachpost.save()
                context = {'eachpost': eachpost,
                           'postid': postid}
                return render(request, 'post_detail.html', context)
            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1
                eachpost.save()
                context = {'eachpost': eachpost,
                           'postid': postid}
                return render(request, 'post_detail.html', context)
        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.post = eachpost
            upref.value = userpreference
            userpreference = int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes += 1
            upref.save()
            eachpost.save()
            context = {'eachpost': eachpost,
                       'postid': postid}
            return render(request, 'post_detail.html', context)
    else:
        eachpost = get_object_or_404(Post, id=postid)
        context = {'eachpost': eachpost,
                   'postid': postid}
        return render(request, 'post_detail.html', context)


def like_post(request):
    liked = False
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.get(id=int(post_id))
        # post = Post.objects.all()
        if request.session.get('has_liked_'+post_id, liked):
            print("unlike")
            if post.likes > 0:
                likes = post.likes - 1
                try:
                    del request.session['has_liked_'+post_id]
                except KeyError:
                    print("keyerror")
        else:
            print("like")
            request.session['has_liked_'+post_id] = True
            likes = post.likes + 1
    post.likes = likes
    post.save()
    return HttpResponse(likes, liked)


def display_image(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    post_id = instance.pk
    image = Images.objects.filter(post=post_id)
    context = {
        "image": image,
    }
    return render(request, "delete_image.html", context)
