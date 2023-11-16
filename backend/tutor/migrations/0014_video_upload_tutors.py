# Generated by Django 4.2.5 on 2023-10-17 17:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tutor", "0013_alter_video_upload_v_upload"),
    ]

    operations = [
        migrations.AddField(
            model_name="video_upload",
            name="tutors",
            field=models.ManyToManyField(
                blank=True, related_name="videos", to="tutor.tutor"
            ),
        ),
    ]
