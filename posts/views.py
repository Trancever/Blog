from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from comments.models import Comment
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm


# Create your views here.
class PostCreateView(UserPassesTestMixin, CreateView):
    form_class = PostForm
    template_name = "post_form.html"
    model = Post
    login_url = reverse_lazy("posts:list")

    def get_success_url(self):
        return reverse("posts:detail", kwargs={"slug": self.object.slug})

    def test_func(self):
        return (self.request.user.is_superuser and self.request.user.is_staff)


class PostDetailView(UserPassesTestMixin, TemplateView):
    form_class = CommentForm
    template_name = "post_detail.html"
    login_url = reverse_lazy("posts:list")

    def dispatch(self, request, *args, **kwargs):
        instance_slug = self.kwargs.get("slug")
        self.instance = get_object_or_404(Post, slug=instance_slug)
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        if self.instance.draft or self.instance.publish > timezone.now().date():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                return False
        return True

    def get(self, request, *args, **kwargs):
        initial_data = {
            "content_type": self.instance.get_content_type,
            "object_id": self.instance.id,
        }
        comment_form = self.form_class(initial=initial_data)
        context_data = {
            "object": self.instance,
            "comment_form": comment_form,
        }

        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        # Removing post
        if request.POST.get('post_title') is not None:
            self.instance.delete()
            messages.success(request, "Post successfully deleted")
            return HttpResponseRedirect(reverse_lazy("posts:list"))

        initial_data = {
            "content_type": self.instance.get_content_type,
            "object_id": self.instance.id,
        }
        # Adding comment
        comment_form = self.form_class(request.POST or None, initial=initial_data)
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

        context_data = {
            "object": self.instance,
            "comment_form": comment_form,
        }
        return render(request, self.template_name, context_data)



class PostsListView(TemplateView):
    template_name = "post_list.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            queryset_list = Post.objects.all()
        else:
            queryset_list = Post.objects.active()

        query = request.GET.get("query")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()

        paginator = Paginator(queryset_list, 5)
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        today = timezone.now().date()

        context_data = {
            "objects_list": queryset,
            "page_request_var": page_request_var,
            "today": today,
        }

        return render(request, self.template_name, context_data)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    form_class = PostForm
    template_name = "post_form.html"
    model = Post
    login_url = reverse_lazy("posts:list")

    def get_success_url(self):
        return reverse("posts:detail", kwargs={"slug": self.object.slug})

    def test_func(self):
        return (self.request.user.is_superuser and self.request.user.is_staff)
