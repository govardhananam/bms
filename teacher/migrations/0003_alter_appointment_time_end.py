# Generated by Django 3.2.5 on 2021-09-04 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_alter_appointment_time_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_end',
            field=models.TimeField(blank=True, null=True),
        ),
    ]