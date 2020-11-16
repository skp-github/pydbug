from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist


class CreatedUpdatedAdminMixin(object):
    """

    """
    exclude = ['created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        """

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        obj.save()


class CreatedUpdatedInlineAdminMixin(object):
    """

    """
    exclude = ['created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        """

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        obj.save()


class CreatedUpdatedwithInlineAdminMixin(object):
    """

    """
    exclude = ['created_by', 'updated_by']

    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            if not f.has_changed() and hasattr(f.Meta.model, 'created_by'):
                f.instance.created_by = request.user
            elif f.has_changed() and hasattr(f.Meta.model, 'created_by'):
                try:
                    f.instance.created_by
                except ObjectDoesNotExist:
                    f.instance.created_by = request.user

            if f.has_changed() and hasattr(f.Meta.model, 'updated_by'):
                f.instance.updated_by = request.user
            # f.instance.save()
        formset.save()

    def save_model(self, request, obj, form, change):
        """

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        obj.save()
