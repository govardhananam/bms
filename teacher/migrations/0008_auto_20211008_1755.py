# Generated by Django 3.2.5 on 2021-10-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_remove_appointment_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='c_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='u_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
