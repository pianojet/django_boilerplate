import uuid

from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
        PasswordChangeForm, SetPasswordForm)
from django import forms
from django.forms import ModelForm, EmailField, CharField, ValidationError, HiddenInput
from django.utils import encoding


class LoginForm(AuthenticationForm):
    username = EmailField(label=("Email"))


class UserForm(ModelForm):
    """ form for usage in admin """
    username = CharField(widget=HiddenInput(), required=False)
    password = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = User
        #exclude = ('password',)

    def clean_username(self):
        try:
            username = self.instance.username
        except:
            username = None

        if not username:
            username = uuid.uuid4().hex[:30]
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.id).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            return UNUSABLE_PASSWORD
        else:
            return password