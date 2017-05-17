#!/usr/bin/env python
# -*- coding: utf-8 -*-

from allauth.account.forms import LoginForm


class MyLoginForm(LoginForm):
    """Form subclassing AllAuth LoginForm to change labels and placeholders"""
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Hasło'
        self.fields['login'].label = 'Nazwa użytkownika'
        self.fields['remember'].label = 'Zapamiętaj'
        self.fields['login'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'