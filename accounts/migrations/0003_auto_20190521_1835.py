# Generated by Django 2.0.1 on 2019-05-21 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20190521_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=70, verbose_name='name')),
                ('code', models.CharField(max_length=15, verbose_name='code')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts_accesstype_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts_accesstype_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='access_type',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='access_type', to='accounts.AccessType'),
        ),
    ]
