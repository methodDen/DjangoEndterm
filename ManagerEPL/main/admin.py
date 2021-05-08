from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import Stadium, Match, PlayerStatistics, TeamStatistics, FootballClub, Contract, Agent, Player, Coach


# Register your models here.


@admin.register(Stadium)
class StadiumAdmin(ModelAdmin):
    list_display = ('id', 'name', 'capacity', 'address')
    search_fields = ('name', 'address')
    ordering = ('-capacity',)


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ('id', 'football_club', 'opponent', 'final_score', 'date', 'is_played')
    search_fields = ('football_club', 'opponent')
    ordering = ('date',)


@admin.register(PlayerStatistics)
class PlayerStatisticsAdmin(ModelAdmin):
    list_display = ('id', 'matches_played', 'goals_scored', 'assists', 'yellow_cards', 'is_injured')


@admin.register(TeamStatistics)
class TeamStatisticsAdmin(ModelAdmin):
    list_display = ('id', 'wins', 'draws', 'loses', 'points', 'place')
    ordering = ('place',)


@admin.register(FootballClub)
class FootballClubAdmin(ModelAdmin):
    list_display = ('id', 'title', 'website', 'team_statistics', 'stadium')
    search_fields = ('title',)
    ordering = ('team_statistics__place',)


@admin.register(Contract)
class ContractAdmin(ModelAdmin):
    list_display = ('id', 'signing_date', 'expiration_date', 'salary')
    ordering = ('-salary',)


@admin.register(Agent)
class AgentAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age', 'nationality')
    search_fields = ('first_name', 'last_name')


@admin.register(Player)
class PlayerAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age', 'nationality', 'football_club')
    search_fields = ('first_name', 'last_name')


@admin.register(Coach)
class CoachAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age', 'nationality', 'post', 'football_club')
    search_fields = ('first_name', 'last_name')
