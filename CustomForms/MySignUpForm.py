#!/usr/bin/env python
# -*- coding: utf-8 -*-

from allauth.account.forms import SignupForm


class MySignUpForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MySignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
        self.fields['email'].label = 'Adres e-mail'
        self.fields['email'].widget.attrs['placeholder'] = 'Adres e-mail'
        self.fields['email'].required = True
        self.fields['password1'].label = 'Hasło'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password2'].label = 'Powtórz Hasło'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz Hasło'