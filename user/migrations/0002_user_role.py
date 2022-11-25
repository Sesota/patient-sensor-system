# Generated by Django 4.1.3 on 2022-11-25 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("patient", "Patient"),
                    ("supervisor", "Supervisor"),
                ],
                default="admin",
                max_length=10,
            ),
        ),
    ]