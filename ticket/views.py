from datetime import datetime

from dateutil.parser import parse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from accounts.models import Profile
from pydbug.views import CreatedUpdatedViewSetMixin
from ticket.forms import TicketForm, TeamForm
from ticket.models import Team, PeopleToTeam, TicketFile, Ticket, Organisation, Department, TeamAccessLevel, \
    TicketComment, UserGroupToPeople, UserGroup, PeopleToOrg
from ticket.serializers import TicketFileSerializer, UserSerializer, OrganisationSerializer, DepartmentSerializer, \
    ProfileSerializer, TicketCommentSerializer, TicketSerializer, UserGroupSerializer, UserGroupToPeopleSerializer, \
    OrganisationModelSerializer

# Create your views here.
User = get_user_model()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100000


class ListProject(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'ticket/list-project.html'
    paginate_by = 10

    def get_queryset(self):
        return PeopleToTeam.objects.filter(people=self.request.user.profile)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['starred_projects'] = 0
        context['level0'] = True
        projects_list = PeopleToTeam.objects.filter(people=self.request.user.profile).values_list('team_id', flat=True)
        projects_list = list(projects_list)
        context['created_projects'] = Team.objects.filter(created_by=self.request.user).exclude(id__in=projects_list)
        context['projects_count'] = len(projects_list) + len(context['created_projects'])
        return context


class ListGroups(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'ticket/list-groups.html'
    paginate_by = 10

    def get_queryset(self):
        return UserGroup.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['starred_projects'] = 0
        context['level1'] = True
        projects_list = PeopleToTeam.objects.filter(people=self.request.user.profile).values_list('team_id', flat=True)
        projects_list = list(projects_list)
        context['created_projects'] = Team.objects.filter(created_by=self.request.user).exclude(id__in=projects_list)
        context['projects_count'] = len(projects_list) + len(context['created_projects'])
        context['team_id'] = self.kwargs['team_id']
        return context


class TeamCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamForm
    template_name = 'ticket/create-project.html'

    def get_success_url(self):
        return reverse_lazy('list_project')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user

        instance = super().form_valid(form)
        if form.data.get('project_owner') == form.data.get('project_lead'):
            people_owner_obj = PeopleToTeam()
            people_owner_obj.people = Profile.objects.get(id=form.data.get('project_owner'))
            people_owner_obj.team = form.instance
            people_owner_obj.created_by, people_owner_obj.updated_by = self.request.user, self.request.user
            people_owner_obj.save()
            owner_obj, maintainer_obj = TeamAccessLevel(), TeamAccessLevel()
            owner_obj.p2t, maintainer_obj.p2t = people_owner_obj, people_owner_obj
            owner_obj.created_by, maintainer_obj.created_by = self.request.user, self.request.user
            owner_obj.updated_by, maintainer_obj.updated_by = self.request.user, self.request.user
            owner_obj.access_type = 0
            maintainer_obj.access_type = 1
            owner_obj.save()
            maintainer_obj.save()
        else:
            people_owner_obj, people_lead_obj = PeopleToTeam(), PeopleToTeam()
            people_owner_obj.people, people_lead_obj.people = Profile.objects.get(
                id=form.data.get('project_owner')), Profile.objects.get(id=form.data.get('project_lead'))
            people_owner_obj.team, people_lead_obj.team = form.instance, form.instance
            people_owner_obj.created_by, people_owner_obj.updated_by = self.request.user, self.request.user
            people_lead_obj.created_by, people_lead_obj.updated_by = self.request.user, self.request.user
            people_owner_obj.save()
            people_lead_obj.save()
            owner_obj, maintainer_obj = TeamAccessLevel(), TeamAccessLevel()
            owner_obj.p2t, maintainer_obj.p2t = people_owner_obj, people_lead_obj
            owner_obj.created_by, maintainer_obj.created_by = self.request.user, self.request.user
            owner_obj.updated_by, maintainer_obj.updated_by = self.request.user, self.request.user
            owner_obj.access_type = 0
            maintainer_obj.access_type = 1
            owner_obj.save()
            maintainer_obj.save()

        # TODO: Send email/notification to user assigned

        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['projects_count'] = PeopleToTeam.objects.filter(people=self.request.user.profile).count()
        context['starred_projects'] = 0

        return context


class ListPendingAgreement(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/approval-list.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(Q(assigned_to=self.request.user.profile) | Q(created_by=self.request.user),
                                     status=0, ticket_type=1,
                                     project_name_id=self.kwargs['team_id']).order_by('-modified')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement List'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class ListOpenRequirement(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/open-requirement-list.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(Q(assigned_to=self.request.user.profile) | Q(created_by=self.request.user),
                                     status=1, ticket_type=1, project_name=self.kwargs['team_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Open Requirement List'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']

        return context


class ListFeatures(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list-feature.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(Q(assigned_to=self.request.user.profile) | Q(created_by=self.request.user),
                                     status__in=[1, 2, 3, 4, 5],
                                     ticket_type=2, project_name=self.kwargs['team_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Open Features List'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']

        return context


class ListBugs(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list-bugs.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(Q(assigned_to=self.request.user.profile) | Q(created_by=self.request.user),
                                     status__in=[1, 2, 3, 4, 5],
                                     ticket_type=3, project_name=self.kwargs['team_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Open Bugs List'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']

        return context


class PendingAgreementDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ticket/issue-detail.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(status=0, id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement Detail'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class OpenFeatureDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ticket/open-feature-detail.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(Q(assigned_to=self.request.user.profile) | Q(created_by=self.request.user),
                                     status__in=[1, 2, 3, 4, 5],
                                     ticket_type=2, project_name=self.kwargs['team_id'], id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement Detail'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class OpenBugDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ticket/open-bug-detail.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(Q(assigned_to=self.request.user.profile) | Q(created_by=self.request.user),
                                     status__in=[1, 2, 3, 4, 5],
                                     ticket_type=3, project_name=self.kwargs['team_id'], id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement Detail'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class OpenRequirementDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ticket/open-requirement-detail.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(status=1, id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement Detail'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class AddMemberListView(LoginRequiredMixin, ListView):
    model = PeopleToTeam
    template_name = 'ticket/add-member.html'
    paginate_by = 10

    def get_queryset(self):
        return Profile.objects.exclude(
            people_to_profile__in=PeopleToTeam.objects.filter(team_id=self.kwargs['team_id']).values_list('id'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement List'
        context['team_list'] = PeopleToTeam.objects.filter(team_id=self.kwargs['team_id'])
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class AddMemberInGroupListView(LoginRequiredMixin, ListView):
    model = UserGroupToPeople
    template_name = 'ticket/add-member-group.html'
    paginate_by = 10

    def get_queryset(self):
        return UserGroupToPeople.objects.filter(group_id=self.kwargs['group_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement List'
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class ProjectMemberListView(LoginRequiredMixin, ListView):
    model = PeopleToTeam
    template_name = 'ticket/org-member-user-list.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('org_id', None):
            return Profile.objects.exclude(
                profile_to_people__in=PeopleToOrg.objects.filter(org=self.request.GET.get('org_id')).values_list('id'))
        else:
            return []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Agreement List'
        context['team_list'] = PeopleToOrg.objects.filter(org=self.request.GET.get('org_id'))
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    """

    """
    form_class = TicketForm
    template_name = 'ticket/create-issue.html'

    def get_success_url(self):
        if self.object.status == 1:
            return reverse_lazy('open_requirement_list', kwargs={'team_id': self.kwargs['team_id']})
        elif self.object.status == 2:
            return reverse_lazy('list_features', kwargs={'team_id': self.kwargs['team_id']})
        return reverse_lazy('agreement_issue_list', kwargs={'team_id': self.kwargs['team_id']})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.project_name = Team.objects.get(id=self.kwargs['team_id'])
        if self.kwargs.get('ticket_id', None):
            form.instance.old_ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
            form.instance.status = 1
        files = []

        for key in form.data.keys():
            if key.startswith('upfiles'):
                files.append(key.split('_')[1])

        instance = super().form_valid(form)
        for file_id in files:
            file_obj = TicketFile.objects.get(id=file_id)
            file_obj.ticket = form.instance
            file_obj.save()

        # TODO: Send email/notification to user assigned

        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        context['section'] = 'Issue'
        if self.kwargs.get('ticket_id', None):
            context['old_ticket'] = self.kwargs['ticket_id']
        context['level1'] = True
        context['team_id'] = self.kwargs['team_id']
        return context


class TicketFileViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """
     Informationfiles viewset for listing , creating , updating and destroying InformationFiles instances
    """
    queryset = TicketFile.objects.all()
    serializer_class = TicketFileSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return User.objects.filter(profile__people_to_profile__team=self.request.GET.get('team_id')).exclude(
            profile__people_to_profile__people_id__isnull=True)


class ProfileViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.GET.get('project_id', None):
            if self.request.GET.get('ticket_view', None):
                return Profile.objects.filter(
                    people_to_profile__in=PeopleToTeam.objects.filter(
                        team_id=self.request.GET.get('project_id')).values_list('id'))
            else:
                return Profile.objects.exclude(
                    people_to_profile__in=PeopleToTeam.objects.filter(
                        team_id=self.request.GET.get('project_id')).values_list('id'))
        else:
            return Profile.objects.filter(user__is_superuser=False, user__is_active=True)


class OrganisationViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """
     Informationfiles viewset for listing , creating , updating and destroying InformationFiles instances
    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    pagination_class = LargeResultsSetPagination


class DepartmentViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """

    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_fields = ('organisation',)
    pagination_class = LargeResultsSetPagination


class TeamAccessTypeAddUpdateView(LoginRequiredMixin, GenericAPIView):

    def post(self, request, *args, **kwargs):
        p2t_obj = PeopleToTeam(people_id=self.request.data.get('user_id'), team_id=self.request.data.get('team_id'),
                               created_by=self.request.user, updated_by=self.request.user)
        p2t_obj.save()
        access_obj = TeamAccessLevel(p2t=p2t_obj, access_type=self.request.data.get('status_type'),
                                     created_by=self.request.user, updated_by=self.request.user)
        access_obj.save()
        return Response({'status': 'OKAY'}, HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        access_obj = TeamAccessLevel.objects.filter(p2t_id=self.request.data.get('user_id'),
                                                    access_type=self.request.data.get('old_status')).first()
        access_obj.access_type = self.request.data.get('status_type')
        access_obj.updated_by = self.request.user
        access_obj.save()
        return Response({'status': 'OKAY'}, HTTP_200_OK)


class PeopleToOrgAddUpdateView(LoginRequiredMixin, GenericAPIView):

    def post(self, request, *args, **kwargs):
        p2o_obj = PeopleToOrg(people_id=self.request.data.get('user_id'), org_id=self.request.data.get('org_id'),
                              created_by=self.request.user, updated_by=self.request.user)
        p2o_obj.save()
        return Response({'status': 'OKAY'}, HTTP_200_OK)


class TicketCommentViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """
        TicketComment viewset for listing , creating , updating and destroying InformationComment instances
    """
    queryset = TicketComment.objects.all()
    serializer_class = TicketCommentSerializer

    def post_perform(self, serializer, instance):
        instance.ticket.modified = datetime.now()
        instance.ticket.save()


# class TicketUpdateView(LoginRequiredMixin, UpdateView):
#     """
#
#     """
#     form_class = TicketForm
#     model = Ticket
#
#     def get_success_url(self):
#         return reverse_lazy('information_list_view')
#
#     def form_valid(self, form):
#         import pdb;pdb.set_trace()
#         form.instance.updated_by = self.request.user
#         instance = super().form_valid(form)
#
#         comment = self.request.POST.get('comment', None)
#
#         return instance
#
#     def get_context_data(self, **kwargs):
#
#         ctx = super().get_context_data(**kwargs)
#         return ctx


class TicketViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """
    Information viewset for listing , creating , updating and destroying Information instances
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def patch(self, request, *args, **kwargs):
        """

        :param serializer:
        :param instance:
        :return:
        """
        if self.request.data.get('expected_date', None):
            ticket_obj = Ticket.objects.get(id=self.request.data.get('id'))
            ticket_obj.expected_date = parse(self.request.data.get('expected_date'))
            ticket_obj.updated_by = self.request.user
            ticket_obj.modified = datetime.now()
            ticket_obj.save()
        elif self.request.data.get('update_status', None):

            ticket_obj = Ticket.objects.get(id=self.request.data.get('id'))
            ticket_obj.status = self.request.data.get('status')
            ticket_obj.updated_by = self.request.user
            ticket_obj.modified = datetime.now()
            ticket_obj.save()
        else:
            ticket_obj = Ticket.objects.get(id=self.request.data.get('id'))
            ticket_obj.status = 1
            ticket_obj.modified = datetime.now()
            ticket_obj.save()

        return Response({'message': 'success'}, status=HTTP_200_OK)


class UserGroupViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """
        TicketComment viewset for listing , creating , updating and destroying InformationComment instances
    """
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer


class UserGroupToPeopleViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """
        TicketComment viewset for listing , creating , updating and destroying InformationComment instances
    """
    queryset = UserGroupToPeople.objects.all()
    serializer_class = UserGroupToPeopleSerializer


class OrganisationModelViewSet(CreatedUpdatedViewSetMixin, viewsets.ModelViewSet):
    """

    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationModelSerializer

    def get_queryset(self):
        return Organisation.objects.filter(created_by=self.request.user)
