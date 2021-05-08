# Generated by Django 3.1.7 on 2021-05-07 18:15

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_player_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[main.models.age_range_validation], verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Национальность'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[main.models.age_range_validation], verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Национальность'),
        ),
        migrations.AlterField(
            model_name='player',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[main.models.age_range_validation], verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='player',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='player',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Национальность'),
        ),
    ]
