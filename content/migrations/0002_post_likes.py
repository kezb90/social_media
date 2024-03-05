# Generated by Django 4.2.10 on 2024-03-05 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="liked_posts",
                through="content.Like",
                to="accounts.profile",
            ),
        ),
    ]