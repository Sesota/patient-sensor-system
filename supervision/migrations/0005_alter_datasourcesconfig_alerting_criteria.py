# Generated by Django 4.1.3 on 2022-11-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supervision", "0004_datasourcesconfig_alerting_criteria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datasourcesconfig",
            name="alerting_criteria",
            field=models.CharField(
                blank=True,
                default="0",
                help_text="Alerting criteria for this datasource",
                max_length=255,
            ),
        ),
    ]