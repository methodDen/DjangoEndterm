from django.shortcuts import render
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, AllowAny
from main.models import Player, TeamStatistics, PlayerStatistics, Stadium, FootballClub, Match, Contract, Agent, Coach
from main.serializers import PlayerMatchesSerializer, PlayerRepresentationSerializer, PlayerFullSerializer, \
    PlayerContractSerializer, \
    TeamStatisticsSerializer, TeamStatisticsFullSerializer, PlayerStatisticsSerializer, PlayerStatisticsFullSerializer, \
    StadiumSerializer, \
    StadiumFullSerializer, FootballClubRepresentationSerializer, FootballClubFullSerializer, MatchSerializer, \
    MatchFullSerializer, \
    ContractSerializer, ContractFullSerializer, AgentSerializer, CoachSerializer, CoachFullSerializer

# Create your views here.

logger = logging.getLogger(__name__)


class StadiumViewSet(viewsets.ModelViewSet):
    queryset = Stadium.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StadiumSerializer
        else:
            return StadiumFullSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Stadium is created: {serializer.instance}')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Stadium is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Stadium is deleted, {instance}')


class PlayerStatisticsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatistics.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayerStatisticsSerializer
        else:
            return PlayerStatisticsFullSerializer

    def get_permissions(self):
        if self.action in ['list', 'get_top_scorer_stats', 'get_top_assistant_stats']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Player Statistics is created: {serializer.instance}')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Player Statistics is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Player Statistics is deleted, {instance}')

    @action(methods=['GET'], detail=False, url_path='top-scorers')
    def get_top_scorer_stats(self, request):
        queryset = PlayerStatistics.objects.top_goalscorers_stats()
        serializer = PlayerStatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='top-assistants')
    def get_top_assistant_stats(self, request):
        queryset = PlayerStatistics.objects.top_assistant_stats()
        serializer = PlayerStatisticsSerializer(queryset, many=True)
        return Response(serializer.data)


class TeamStatisticsViewSet(viewsets.ModelViewSet):
    queryset = TeamStatistics.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamStatisticsSerializer
        else:
            return TeamStatisticsFullSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Team Statistics is created: {serializer.instance}')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Team Statistics is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Team Statistics is deleted, {instance}')


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayerRepresentationSerializer
        else:
            return PlayerFullSerializer

    def get_permissions(self):
        if self.action in ['list', 'get_local_players', 'player_matches_statistics',
                           'get_foreign_players', 'get_injured_players', 'get_healthy_players',
                           'get_player_and_contract']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Player is created: {serializer.instance}')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Player is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Player is deleted, {instance}')

    @action(methods=['GET'], detail=True, url_path='stats')
    def player_matches_statistics(self, request, pk):
        queryset = Player.objects.get_related_statistics(pk)
        # Обязательно ли ставить False перед many?
        serializer = PlayerMatchesSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='local')
    def get_local_players(self, request):
        queryset = Player.objects.get_players_from_academy()
        serializer = PlayerRepresentationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='foreign')
    def get_foreign_players(self, request):
        queryset = Player.objects.get_foreign_players()
        serializer = PlayerRepresentationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='injured')
    def get_injured_players(self, request):
        queryset = Player.objects.get_injured_players()
        serializer = PlayerRepresentationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='healthy')
    def get_healthy_players(self, request):
        queryset = Player.objects.get_not_injured_players()
        serializer = PlayerRepresentationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='contract')
    def get_player_and_contract(self, request, pk):
        queryset = Player.objects.filter(pk=pk)
        serializer = PlayerContractSerializer(queryset, many=True)
        return Response(serializer.data)


class FootballClubViewSet(viewsets.ModelViewSet):  # Стоит ли создавать тотальный апдейт-сериализатор?

    queryset = FootballClub.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return FootballClubRepresentationSerializer
        else:
            return FootballClubFullSerializer

    def get_permissions(self):
        if self.action in ['list', 'get_football_club_by_place']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]



    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Football Club is deleted, {instance}')

    @action(methods=['GET'], detail=True, url_path='place')
    def get_football_club_by_place(self, request, pk):
        queryset = FootballClub.objects.get_by_place_with_relation(place=pk)
        serializer = FootballClubRepresentationSerializer(queryset, many=True)
        return Response(serializer.data)


class MatchViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return MatchSerializer
        else:
            return MatchFullSerializer

    def get_permissions(self):
        if self.action in ['list', 'get_match_by_opponent']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    queryset = Match.objects.all()

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Match is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Match is deleted, {instance}')

    @action(methods=['GET'], detail=True, url_path='opponent')
    def get_match_by_opponent(self, request, pk):
        queryset = Match.objects.get_by_opponent(opponent=pk)
        serializer = MatchSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='weather')
    def get_match_by_weather(self, request, pk):
        queryset = Match.objects.get_by_weather(weather=pk)
        serializer = MatchFullSerializer(queryset, many=True)
        return Response(serializer.data)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ContractSerializer
        else:
            return ContractFullSerializer

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Contract is created: {serializer.instance}')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Contract is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Contract is deleted, {instance}')


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()

    serializer_class = AgentSerializer

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Agent is created: {serializer.instance}')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Agent is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Agent is deleted, {instance}')

    @action(methods=['GET'], detail=False, url_path='experienced')
    def get_experienced_agents(self, request):
        queryset = Agent.objects.get_experienced()
        serializer = AgentSerializer(queryset, many=True)
        return Response(serializer.data)


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CoachSerializer
        else:
            return CoachFullSerializer

    def get_permissions(self):
        if self.action in ['list', 'get_coaches_by_football_club']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Coach is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Coach is deleted, {instance}')

    @action(methods=['GET'], detail=True, url_path='football_club')
    def get_coaches_by_football_club(self, request, pk):
        queryset = Coach.objects.get_by_football_club_with_relation(football_club_id=pk)
        serializer = CoachSerializer(queryset, many=True)
        return Response(serializer.data)
