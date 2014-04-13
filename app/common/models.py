from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'auth_user_profile'
