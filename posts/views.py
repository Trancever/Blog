from urllib import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm


# Create your views here.

def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Successfully Created")

    context = {
        "form": form
    }
    return render(request, "post_form.html", context)


def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    # Deleting comment
    try:
        comment_to_delete_id = int(request.POST.get("comment_id"))
    except:
        comment_to_delete_id = None

    if comment_to_delete_id is not None:
        comment_qs = Comment.objects.filter(id=comment_to_delete_id)
        if comment_qs.exists() and comment_qs.count() == 1:
            comment_to_delete = comment_qs.first()
            if comment_to_delete.children.count() != 0:
                for child in comment_to_delete.children:
                    child.delete()
            comment_to_delete.delete()
            return HttpResponseRedirect(instance.get_absolute_url())

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    # Adding comment
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get("object_id")
        content = comment_form.cleaned_data.get("content")

        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id is not None:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content,
            parent=parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    user = request.user

    context_data = {
        "object": instance,
        "share_string": share_string,
        "comment_form": comment_form,
        # "user": user
    }
    return render(request, "post_detail.html", context_data)


def posts_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("query")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 10)  # Show 10 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context_data = {
        "objects_list": queryset,
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", context_data)


def posts_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Saved")

    context_data = {
        "object": instance,
        "form": form
    }
    return render(request, "post_form.html", context_data)


def posts_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")
