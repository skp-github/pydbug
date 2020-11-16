# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CreatedUpdatedModel(models.Model):
    """ CreatedUpdatedModel
    An abstract base class model that provides self-managed "created_by" and
    "updated_by" fields.
    """
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created", verbose_name=_('created by'),
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_updated", verbose_name=_('updated by'),
                                   on_delete=models.CASCADE)

    class Meta:
        abstract = True
