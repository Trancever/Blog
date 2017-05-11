"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from .views import (
    posts_list,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
)

urlpatterns = [
    url(r'^create$', PostCreateView.as_view(), name="create"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="detail"),
    url(r'^$', posts_list, name="list"),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateView.as_view(), name="update"),
]
