# Generated by Django 4.0.2 on 2022-10-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_alter_group_enable_black_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='enable_black_list',
            field=models.BooleanField(default=False, verbose_name='Вкл/Выкл черный список'),
        ),
    ]
