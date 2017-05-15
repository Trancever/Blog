#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms


class ContactForm(forms.Form):
    fullname = forms.CharField(max_length=100, label="Imię i nazwisko", required=True,
                               error_messages={"required": "To pole jest wymagane."})
    email = forms.EmailField(label="Adres E-mail", required=True, error_messages={"required": "To pole jest wymagane."})
    message = forms.CharField(max_length=1000, required=True, label="Wiadomość",
                              error_messages={"required": "To pole jest wymagane."}, widget=forms.Textarea)

    def clean_email(self):
        return self.cleaned_data.get("email")

    def clean_fullname(self):
        name = self.cleaned_data.get("fullname")
        if len(name) < 3:
            raise forms.ValidationError("Fullname must contains at least 3 characters.")
        return name
