# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from versatileimagefield.fields import VersatileImageField

from pydbug.models import CreatedUpdatedModel

ACCESS_TYPE = (
    (0, _('OWNER')),
    (1, _('MAINTAINER')),
    (2, _('DEVELOPER')),
    (3, _('REPORTER')),
    (4, _('GUEST')),
    (5, _('OTHERS')),

)


class Profile(models.Model):
    """
    User profile to handle extra fields as per requirement
    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    access_type = models.PositiveIntegerField(choices=ACCESS_TYPE, default=5)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = VersatileImageField(null=True, blank=True, max_length=500)
    age = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=256, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

