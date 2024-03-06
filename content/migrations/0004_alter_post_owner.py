# Generated by Django 4.2.10 on 2024-03-06 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_followrequest_accepted"),
        ("content", "0003_story_storyvideo_storyimage_storyaudio_storyviewer_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="accounts.profile",
            ),
        ),
    ]
