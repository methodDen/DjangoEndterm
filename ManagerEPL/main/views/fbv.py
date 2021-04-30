from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from main.models import Stadium, Match, PlayerStatistics, TeamStatistics
from main.serializers import MatchSeparateSerializer, StadiumFullSerializer, PlayerStatisticsFullSerializer, \
    TeamStatisticsFullSerializer

#Добавлять ли PS и TS?

@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def stadium_list(request):
    if request.method == 'GET':
        stadiums = Stadium.objects.all()
        serializer = StadiumFullSerializer(stadiums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StadiumFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def stadium_detail(request, pk):
    try:
        stadium = Stadium.objects.get(pk=pk)
    except Stadium.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StadiumFullSerializer(stadium)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StadiumFullSerializer(stadium, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stadium.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def match_list(request):
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSeparateSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MatchSeparateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def match_detail(request, pk):
    try:
        match = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchSeparateSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MatchSeparateSerializer(match, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
