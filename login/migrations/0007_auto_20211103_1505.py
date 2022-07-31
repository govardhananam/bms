# Generated by Django 3.2.5 on 2021-11-03 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_merge_20211011_1348'),
        ('login', '0006_auto_20211103_1105'),
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