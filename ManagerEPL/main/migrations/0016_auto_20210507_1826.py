# Generated by Django 3.1.7 on 2021-05-07 12:26

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20210507_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='coach_photos', validators=[utils.validators.validate_size, utils.validators.validate_extension], verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='player',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='player_photos', validators=[utils.validators.validate_size, utils.validators.validate_extension], verbose_name='Фото'),
        ),
    ]
