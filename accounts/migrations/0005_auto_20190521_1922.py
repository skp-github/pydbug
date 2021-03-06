# Generated by Django 2.0.1 on 2019-05-21 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190521_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesstype',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='accesstype',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='profile',
            name='access_type',
            field=models.PositiveIntegerField(choices=[(1, 'MAINTAINER'), (2, 'DEVELOPER'), (3, 'REPORTER'), (4, 'GUEST'), (5, 'OTHERS')], default=5),
        ),
        migrations.DeleteModel(
            name='AccessType',
        ),
    ]
