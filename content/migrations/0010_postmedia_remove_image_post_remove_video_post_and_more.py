# Generated by Django 4.2.10 on 2024-03-07 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0009_alter_viewerpost_post"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostMedia",
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
                (
                    "media",
                    models.FileField(
                        upload_to="media/content/post/", verbose_name="media of post"
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name="image",
            name="post",
        ),
        migrations.RemoveField(
            model_name="video",
            name="post",
        ),
        migrations.AlterField(
            model_name="like",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="mention",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="post",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="story",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="storyaudio",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="storyimage",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="storyvideo",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="storyviewer",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.DeleteModel(
            name="Audio",
        ),
        migrations.DeleteModel(
            name="Image",
        ),
        migrations.DeleteModel(
            name="Video",
        ),
        migrations.AddField(
            model_name="postmedia",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_media",
                to="content.post",
                verbose_name="post",
            ),
        ),
    ]
