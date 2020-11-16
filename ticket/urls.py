from django.urls import path
from rest_framework.routers import DefaultRouter

from ticket.views import ListProject, TicketCreateView, TicketFileViewSet, UsersViewSet, OrganisationViewSet,\
                         ListPendingAgreement, TeamCreateView, DepartmentViewSet, ProfileViewSet, AddMemberListView, TeamAccessTypeAddUpdateView, PendingAgreementDetailView,\
                         TicketCommentViewSet, TicketViewSet, ListOpenRequirement, OpenRequirementDetailView, ListGroups, ProjectMemberListView, UserGroupViewSet, AddMemberInGroupListView, \
                         UserGroupToPeopleViewSet, ListFeatures, OpenFeatureDetailView, OrganisationModelViewSet, ListBugs, OpenBugDetailView, PeopleToOrgAddUpdateView

router = DefaultRouter()
router.register(r'ticketfiles', TicketFileViewSet)
router.register(r'ticket', TicketViewSet)
router.register(r'users', UsersViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'organisation', OrganisationViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'comment', TicketCommentViewSet)
router.register(r'user-groups', UserGroupViewSet)
router.register(r'add-user-to-groups', UserGroupToPeopleViewSet)
router.register(r'crud-organisation', OrganisationModelViewSet)



urlpatterns = [
    path('create-issue/<int:team_id>/', TicketCreateView.as_view(), name='create_issue'),
    path('create-feature/<int:team_id>/<int:ticket_id>/', TicketCreateView.as_view(), name='create_feature'),
    path('list-project/', ListProject.as_view(), name='list_project'),
    path('list-features/<int:team_id>', ListFeatures.as_view(), name='list_features'),
    path('list-groups/<int:team_id>/', ListGroups.as_view(), name='list_groups'),
    path('list-bugs/<int:team_id>/', ListBugs.as_view(), name='list_bugs'),
    path('pending-agreement-list/<int:team_id>/', ListPendingAgreement.as_view(), name='agreement_issue_list'),
    path('open-requirements-list/<int:team_id>/', ListOpenRequirement.as_view(), name='open_requirement_list'),
    path('open-requirements/<int:pk>/<int:team_id>/', OpenRequirementDetailView.as_view(), name='open_requirement_detail'),
    path('create-project/', TeamCreateView.as_view(), name='create_project'),
    path('members/<int:team_id>/', AddMemberListView.as_view(), name='add_members_project'),
    path('update-user-access/', TeamAccessTypeAddUpdateView.as_view(), name='user_access_type_update'),
    path('update-user-organisation/', PeopleToOrgAddUpdateView.as_view(), name='user_access_org_update'),
    path('pending-agreement/<int:pk>/<int:team_id>/', PendingAgreementDetailView.as_view(), name='pending_agreement_list'),
    path('open-feature/<int:pk>/<int:team_id>/', OpenFeatureDetailView.as_view(), name='feature_detail'),
    path('open-bug/<int:pk>/<int:team_id>/', OpenBugDetailView.as_view(), name='bug_detail'),
    path('project-users-list/<int:team_id>', ProjectMemberListView.as_view(), name='project_member_list'),
    path('group-users-add/<int:team_id>/<int:group_id>/', AddMemberInGroupListView.as_view(), name='add_member_group'),



]
