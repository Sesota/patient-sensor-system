# Generated by Django 4.1.3 on 2022-11-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supervision", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasourcesconfig",
            name="alerting_medium",
            field=models.CharField(
                choices=[("off", "Off"), ("sms", "Sms"), ("email", "Email")],
                default="off",
                max_length=31,
            ),
        ),
    ]