# Generated by Django 5.0.6 on 2024-06-21 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_deleted_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='audio_uploads/'),
        ),
    ]
