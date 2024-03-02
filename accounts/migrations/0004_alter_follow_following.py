# Generated by Django 4.2.10 on 2024-03-02 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0003_follow"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
