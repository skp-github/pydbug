from django import forms

from ticket.models import Ticket, Team


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'priority_type', 'ticket_title',
                  'ticket_description', 'assigned_to', 'old_ticket',
                  'desired_date']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['dept',
                  'team_name',
                  'team_description',
                  'project_id',
                  'vcs_ip']
