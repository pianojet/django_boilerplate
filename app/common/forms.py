import uuid

from notification import models as notification

from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
        PasswordChangeForm, SetPasswordForm)
from django import forms
from django.forms import ModelForm, EmailField, CharField, ValidationError, HiddenInput
from django.utils import encoding
from django.core.exceptions import ObjectDoesNotExist


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

class SignupForm(forms.Form):
  """ 
  Form for creating new login
  """
  email = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
  check_password = forms.CharField(widget=forms.PasswordInput)

  def clean(self):
    try:
      if self.cleaned_data['password'] != self.cleaned_data['check_password']:
        raise forms.ValidationError("Passwords entered do not match")
    except KeyError:
      # didn't find what we expected in data - fields are blank on front end.  Fields
      # are required by default so we don't need to worry about validation
      pass
    return self.cleaned_data


class AppPasswordResetForm(PasswordResetForm):
    def clean_email(self, request=None):
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email, is_active=True)
        if len(self.users_cache) == 0:
            # We want to log the attempt in the authlog.  We have to hardcode
            # the url since the request is not available without modifying the
            # django code.  Unfortunately we can't get the ip address either.
            AuthLog(user=email, requested_url='/password-reset/').save()
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data.get('email', '')#user = self.users_cache
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return

        my_list = []
        my_list.append(user)
        site_name = domain = requested_domain
        c = {
                'email': user.email,
                'from_user' : from_email,
                'domain': domain,
                'uid': int_to_base36(user.pk),
                'user': user,
                'protocol': use_https and 'https' or 'http',
        }
        notification.send_now(my_list, 'forgot_password',c ,sender=from_email)
