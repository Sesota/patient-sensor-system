# Generated by Django 4.1.3 on 2023-02-06 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.validators


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0002_device_last_used_at_alter_device_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("datasource", "0002_heartratedata_device"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heartratedata",
            name="device",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="device.device",
            ),
        ),
        migrations.AlterField(
            model_name="heartratedata",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                validators=[user.validators.UserRoleValidator("patient")],
            ),
        ),
    ]
