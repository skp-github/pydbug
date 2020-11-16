from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from pydbug.admin import CreatedUpdatedInlineAdminMixin
from ticket.models import Organisation, Department, Team, PeopleToTeam, Ticket, TicketFile, TeamAccessLevel, UserGroup, UserGroupToPeople


@admin.register(Organisation)
class OrganisationAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """

@admin.register(Department)
class DepartmentAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """

@admin.register(Team)
class TeamAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
@admin.register(PeopleToTeam)
class PeopleToTeamAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
@admin.register(Ticket)
class TicketAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
@admin.register(TicketFile)
class TicketFileAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
@admin.register(TeamAccessLevel)
class TeamAccessLevelAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
@admin.register(UserGroup)
class UserGroupAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
@admin.register(UserGroupToPeople)
class UserGroupToPeopleAdmin(CreatedUpdatedInlineAdminMixin, admin.ModelAdmin):
    """

    """
