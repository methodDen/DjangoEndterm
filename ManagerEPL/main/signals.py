from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Player, FootballClub, TeamStatistics, PlayerStatistics, Stadium


@receiver(post_save, sender=TeamStatistics)
def team_statistics_created(sender, instance, created, **kwargs):
    if created:
        FootballClub.objects.create(team_statistics=instance)


@receiver(post_save, sender=PlayerStatistics)
def player_statistics_created(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(statistics=instance)


@receiver(post_save, sender=Stadium)
def stadium_created(sender, instance, created, **kwargs):
    if created:
        FootballClub.objects.create(stadium=instance)
