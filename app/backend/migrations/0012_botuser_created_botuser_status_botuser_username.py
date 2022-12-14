# Generated by Django 4.0.2 on 2022-09-14 12:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_template_delete_posts_remove_botuser_km_or_kv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 12, 44, 24, 310080, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='botuser',
            name='status',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user'), ('superadmin', 'superadmin')], default='user', max_length=255),
        ),
        migrations.AddField(
            model_name='botuser',
            name='username',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
