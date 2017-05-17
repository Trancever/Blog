#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from pagedown.widgets import PagedownWidget

from allauth.account.forms import LoginForm

from .models import Post

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
            "tags",
        ]