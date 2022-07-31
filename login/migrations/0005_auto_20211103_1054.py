# Generated by Django 3.2.5 on 2021-11-02 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_merge_20211011_1348'),
        ('login', '0004_alter_user_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='course',
        ),
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.ManyToManyField(blank=True, null=True, to='teacher.course'),
        ),
    ]