from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers

from ticket.models import TicketFile, Ticket, Organisation, TicketComment, UserGroup, UserGroupToPeople


class TicketFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFile
        fields = (
            'id', 'title', 'file_type', 'file', 'ticket')
        read_only_fields = ('meta',)


class UserSerializer(serializers.ModelSerializer):
    """

    """
    text = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj.user.username

    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_code(self, obj):
        return obj.id

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'text',
            'code',
        )


class ProfileSerializer(serializers.ModelSerializer):
    """

    """
    text = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj.user.username

    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_code(self, obj):
        return obj.id

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'text',
            'code',
        )


class OrganisationSerializer(serializers.ModelSerializer):
    """

    """
    text = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj.name

    def get_name(self, obj):
        return obj.name

    def get_code(self, obj):
        return obj.id

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'text',
            'code',
        )


class DepartmentSerializer(serializers.ModelSerializer):
    """

    """
    text = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj.name

    def get_name(self, obj):
        return obj.name

    def get_code(self, obj):
        return obj.id

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'text',
            'code',
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('id', 'group_name')


class OrganisationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('id', 'name')



class UserGroupToPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroupToPeople
        fields = ('id', 'group', 'people')


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ('id', 'text', 'ticket')
