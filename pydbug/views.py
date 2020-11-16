from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class CreatedUpdatedViewSetMixin(object):
    """

    """

    def perform_create(self, serializer, **kwargs):
        """

        :param serializer:
        :return:
        """
        kwargs['created_by'] = self.request.user
        kwargs['updated_by'] = self.request.user
        instance = serializer.save(**kwargs)
        self.post_perform(serializer, instance)

    def perform_update(self, serializer, **kwargs):
        """

        :param serializer:
        :return:
        """
        kwargs['updated_by'] = self.request.user
        instance = serializer.save(**kwargs)
        if not self.request.data.get('edit', None):
            self.post_perform(serializer, instance)

    def post_perform(self, serializer, instance):
        """

        :param serializer:
        :param instance:
        :return:
        """
        pass


class LoginPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """

    """

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """

        for perm in self.get_permission_required():
            if self.request.user.has_perm(perm):
                return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('handler', '403')
