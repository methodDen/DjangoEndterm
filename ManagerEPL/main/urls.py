from main.views.viewsets import PlayerViewSet, TeamStatisticsViewSet, PlayerStatisticsViewSet, \
    StadiumViewSet, FootballClubViewSet, MatchViewSet, \
    ContractViewSet, AgentViewSet, CoachViewSet
from main.views.fbv import stadium_list, stadium_detail, match_list, match_detail
from main.views.cbv import StadiumList, MatchList, ContractList, ContractDetail, PlayerStatisticsList, \
    PlayerStatisticsDetail, TeamStatisticsList, TeamStatisticsDetail

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from django.urls import path

router = routers.SimpleRouter()
router.register('players', PlayerViewSet, basename='players')
router.register('team_stats', TeamStatisticsViewSet, basename='team_stats')
router.register('player_stats', PlayerStatisticsViewSet, basename='player_stats')
router.register('stadiums', StadiumViewSet, basename='stadiums')
router.register('football_clubs', FootballClubViewSet, basename='football_clubs')
router.register('matches', MatchViewSet, basename='matches')
router.register('contracts', ContractViewSet, basename='contracts')
router.register('agents', AgentViewSet, basename='agents')
router.register('coaches', CoachViewSet, basename='coaches')

urlpatterns = []
# urlpatterns = [
#     path('matches/', match_list, name='match_list'),
#     path('matches/<int:pk>/', match_detail, name='match_detail'),
#     path('stadiums/', stadium_list, name='stadium_list'),
#     path('stadiums/<int:pk>/', stadium_detail, name='stadium_detail'),
# ]

# urlpatterns = [
#     path('matches/', MatchList.as_view()),
#     path('stadiums/', StadiumList.as_view()),
#     path('contracts/', ContractList.as_view()),
#     path('contracts/<int:pk>/', ContractDetail.as_view()),
#     path('player_stats/', PlayerStatisticsList.as_view()),
#     path('player_stats/<int:pk>/', PlayerStatisticsDetail.as_view()),
#     path('team_stats/', TeamStatisticsList.as_view()),
#     path('team_stats/<int:pk>/', TeamStatisticsDetail.as_view()),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns += router.urls