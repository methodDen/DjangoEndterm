# Generated by Django 3.1.7 on 2021-05-07 09:04

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_agent_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='agent_photos', validators=[utils.validators.validate_size, utils.validators.validate_extension], verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='footballclub',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='football_club_photos', validators=[utils.validators.validate_size, utils.validators.validate_extension], verbose_name='Эмблема'),
        ),
    ]
