# Generated by Django 2.0.1 on 2019-06-03 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0012_teamaccesslevel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamaccesslevel',
            options={},
        ),
        migrations.RemoveField(
            model_name='team',
            name='project_lead',
        ),
        migrations.RemoveField(
            model_name='team',
            name='project_owner',
        ),
        migrations.AlterUniqueTogether(
            name='teamaccesslevel',
            unique_together={('p2t', 'access_type')},
        ),
    ]
