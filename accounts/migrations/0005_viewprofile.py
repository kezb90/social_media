# Generated by Django 4.2.10 on 2024-03-07 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_remove_followrequest_accepted"),
    ]

    operations = [
        migrations.CreateModel(
            name="ViewProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "viewed_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="viewed_profile",
                        to="accounts.profile",
                    ),
                ),
                (
                    "viewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="viewers_of_profile",
                        to="accounts.profile",
                    ),
                ),
            ],
        ),
    ]
