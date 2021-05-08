# Generated by Django 3.1.7 on 2021-05-07 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210508_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballclub',
            name='stadium',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.stadium', verbose_name='Стадион'),
        ),
        migrations.AlterField(
            model_name='footballclub',
            name='team_statistics',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.teamstatistics', verbose_name='Статистика команды'),
        ),
        migrations.AlterField(
            model_name='footballclub',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='footballclub',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Веб сайт'),
        ),
    ]
