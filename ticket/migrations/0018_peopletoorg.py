# Generated by Django 2.0.1 on 2019-06-18 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190610_1507'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0017_auto_20190610_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeopleToOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_peopletoorg_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_to_org', to='ticket.Organisation')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_to_people', to='accounts.Profile')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_peopletoorg_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
