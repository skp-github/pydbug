from __future__ import unicode_literals

import os
from random import uniform, choice

from PIL import Image
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from moviepy import editor
from sorl.thumbnail import get_thumbnail

from accounts.models import Profile
from pydbug.models import CreatedUpdatedModel
from pydbug.settings import MATERIAL_COLOR_LIST

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
location = lambda x: os.path.join(os.path.realpath(BASE_DIR), x)

TICKET_TYPE = (
    (1, _('REQUIREMENT')),
    (2, _('FEATURE')),
    (3, _('BUG')),
    (4, _('OTHERS')),
)

STATUS_TYPE = (
    (0, _('NEED APPROVAL')),
    (1, _('OPEN')),
    (2, _('CLOSED')),
    (3, _('REPOEN')),
    (4, _('RESOLVED')),
    (5, _('TEST'))
)

PRIORITY_TYPE = (
    (1, _('LOW')),
    (2, _('MODERATE')),
    (3, _('CRITICAL')),
)

FILE_TYPE = (
    (0, _("Image")),
    (1, _("Pdf")),
    (2, _("doc")),
    (3, _("other")),
    (4, _("audio")),
    (5, _("video"))
)

ACCESS_TYPE = (
    (0, _('OWNER')),
    (1, _('MAINTAINER')),
    (2, _('DEVELOPER')),
    (3, _('TESTER')),
    (4, _('REPORTER')),
    (5, _('GUEST')),
    (6, _('OTHERS')),

)

ACCESS_TYPE_COLOR = {
    0: 'primary',
    1: 'success',
    2: 'warning',
    3: 'danger',
    4: 'info',
    5: 'dark',
    6: 'brand'
}


class Organisation(TimeStampedModel, CreatedUpdatedModel):
    name = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return self.name


class Department(TimeStampedModel, CreatedUpdatedModel):
    organisation = models.ForeignKey(Organisation, related_name='dept_org', blank=False, null=False,
                                     on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return self.name


class Team(TimeStampedModel, CreatedUpdatedModel):
    dept = models.ForeignKey(Department, related_name='dept_team', blank=False, null=False, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=256, blank=False, null=False)
    team_description = models.TextField(blank=True, null=True)
    project_id = models.CharField(max_length=256, blank=True, null=True)
    vcs_ip = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.team_name

    def spliced_description(self):
        return self.team_description[:36] + (' \u00A0 ' * (36 - len(self.team_description)))

class UserGroup(TimeStampedModel, CreatedUpdatedModel):
    group_name = models.CharField(unique=True, max_length=250,blank=False, null=False)

    def __str__(self):
        return self.group_name

class UserGroupToPeople(TimeStampedModel, CreatedUpdatedModel):
    people = models.ForeignKey(Profile, related_name='user_profile', on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, related_name='user_group', on_delete=models.CASCADE)

    def __str__(self):
        return self.group.group_name


class Ticket(TimeStampedModel, CreatedUpdatedModel):
    project_name = models.ForeignKey(Team, related_name='project', blank=True, null=True, on_delete=models.CASCADE)
    ticket_type = models.PositiveIntegerField(choices=TICKET_TYPE, default=3)
    priority_type = models.PositiveIntegerField(choices=PRIORITY_TYPE, default=1)
    ticket_title = models.TextField(blank=False, null=False)
    ticket_description = models.TextField(blank=False, null=False)
    assigned_to = models.ForeignKey(Profile, related_name='ticket_assigned', blank=True, on_delete=models.CASCADE)
    old_ticket = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=STATUS_TYPE, default=0)
    desired_date = models.DateTimeField(blank=True, null=True)
    expected_date = models.DateTimeField(blank=True, null=True)
    actual_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.ticket_title

    def priority_to_name(self):
        if self.priority_type == 1:
            return 'LOW'
        elif self.priority_type == 2:
            return 'MODERATE'
        return 'CRITICAL'

    def get_ticket_type(self):
        return [data[1] for data in TICKET_TYPE if data[0] == self.ticket_type][0]

    def get_status_type(self):
        return [data[1] for data in STATUS_TYPE if data[0] == self.status][0]

    def get_status_color(self):
        return ACCESS_TYPE_COLOR[self.status]

    def priority_icon(self):
        if self.priority_type == 1:
            return 'success'
        elif self.priority_type == 2:
            return 'warning'
        return 'danger'

    def get_files(self, user=None, size='48x48'):
        """

        :param user:
        :param size:
        :return:
        """
        files = self.files.all()
        ret = []

        for x in files:
            ret.append({
                "title": x.title,
                'file': x.file.url,
                'file_id': x.id,
                'file_type': x.file_type,
                'thumb': x.get_thumb(size),
            })

        return ret

    def assigned_image_available(self):
        try:
            if self.assigned_to.profile_pic:
                return True
            else:
                return False
        except Exception as e:
            return False


    def get_random_color(self):
        return choice(MATERIAL_COLOR_LIST)


    def get_comments(self):
        return TicketComment.objects.filter(ticket=self)

class TicketFile(TimeStampedModel, CreatedUpdatedModel):
    title = models.CharField(max_length=256, blank=True, null=True)
    file_type = models.PositiveSmallIntegerField(choices=FILE_TYPE)
    file = models.FileField()
    ticket = models.ForeignKey(Ticket, related_name='files', null=True, blank=True, on_delete=models.SET_NULL)



    def get_thumb(self, size='48x48'):
        """

        :param size:
        :return:
        """
        if self.file_type == 0:
            im = get_thumbnail(self.file, size, crop='center', quality=70)
            return im.url
        elif self.file_type == 1:
            return "/media/pdf.png"
        elif self.file_type == 2:
            return "/media/doc.png"
        elif self.file_type == 3:
            return "/media/other.png"
        elif self.file_type == 4:
            return "/media/audio.png"
        elif self.file_type == 5:
            thumb = "{}_{}.jpg".format(".".join(self.file.path.split(".")[0:-1]), size)

            if not os.path.isfile(thumb):
                clip = editor.VideoFileClip(self.file.path)
                clip.save_frame(thumb, t=uniform(0.1, clip.duration))
            thumb_s = get_thumbnail(thumb, size, crop='center', quality=70)
            path = "{}{}".format(thumb_s.storage.location, thumb_s.url).replace("media/media", "media")

            # put a play button
            if not os.path.isfile(thumb):
                img1 = Image.open(path)
                img2 = Image.open(os.path.join(settings.BASE_DIR, "public/media/play.png"))
                img1.paste(img2, ((img1.width // 2) - 24, (img1.height // 2) - 24), mask=img2)
                img1.save(path)

            return thumb_s.url

        return "/media/doc.png"



class TicketComment(TimeStampedModel, CreatedUpdatedModel):
    """

    """
    text = models.TextField()
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)


class TicketFileComment(TimeStampedModel, CreatedUpdatedModel):
    """

    """
    file_type = models.PositiveSmallIntegerField(choices=FILE_TYPE)
    file = models.FileField()
    comment_file = models.ForeignKey(TicketComment, related_name='comment_files', on_delete=models.CASCADE)


class PeopleToTeam(TimeStampedModel, CreatedUpdatedModel):
    people = models.ForeignKey(Profile, related_name='people_to_profile', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='people_to_team', on_delete=models.CASCADE)

    def __str__(self):
        return self.people.user.get_full_name()


class TeamAccessLevel(TimeStampedModel, CreatedUpdatedModel):
    p2t = models.ForeignKey(PeopleToTeam, related_name="access_level", blank=True, null=True,
                            on_delete=models.SET_NULL)
    access_type = models.PositiveIntegerField(choices=ACCESS_TYPE, default=5)

    class Meta:
        unique_together = (('p2t', 'access_type'),)

    def accesstype_to_string(self):
        return [data[1] for data in ACCESS_TYPE if data[0] == self.access_type][0]

    def accesstype_to_color(self):
        return ACCESS_TYPE_COLOR[self.access_type]


class PeopleToOrg(TimeStampedModel, CreatedUpdatedModel):
    people = models.ForeignKey(Profile, related_name='profile_to_people', on_delete=models.CASCADE)
    org = models.ForeignKey(Organisation, related_name='profile_to_org', on_delete=models.CASCADE)

    def __str__(self):
        return self.people.user.get_full_name()


class Project(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class Firstquestion(models.Model):
    first_one = models.TextField()
    first_two = models.TextField()
    first_three = models.TextField()
    first_four = models.TextField()
    first_five = models.TextField()
    first_six = models.TextField()
    first_seven = models.TextField()
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='question_one')