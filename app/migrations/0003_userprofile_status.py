# Generated by Django 3.0.8 on 2021-01-05 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_game_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]