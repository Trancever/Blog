#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class MySignUpForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MySignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
        self.fields['email'].widget.attrs['placeholder'] = 'dupa'


    def signup(self, request, user):
        pass