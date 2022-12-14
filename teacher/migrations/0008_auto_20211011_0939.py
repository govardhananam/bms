# Generated by Django 3.2.5 on 2021-10-10 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_remove_appointment_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('c_id', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together={('u_id', 'name')},
        ),
    ]
