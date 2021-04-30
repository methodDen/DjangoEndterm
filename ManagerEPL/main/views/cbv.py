from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.http import Http404
from main.models import Stadium, Contract, Match, PlayerStatistics, TeamStatistics
from main.serializers import MatchSeparateSerializer, StadiumFullSerializer, PlayerStatisticsFullSerializer, \
    TeamStatisticsFullSerializer, ContractFullSerializer


class StadiumList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        stadiums = Stadium.objects.all()
        serializer = StadiumFullSerializer(stadiums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StadiumFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        matches = Match.objects.all()
        serializer = MatchSeparateSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MatchSeparateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = ContractFullSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContractFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contract = self.get_object(pk)
        serializer = ContractFullSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        contract = self.get_object(pk)
        serializer = ContractFullSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contract = self.get_object(pk)
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerStatisticsList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        player_statistics_many = PlayerStatistics.objects.all()
        serializer = PlayerStatisticsFullSerializer(player_statistics_many, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlayerStatisticsFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerStatisticsDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return PlayerStatistics.objects.get(pk=pk)
        except PlayerStatistics.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        player_statistics = self.get_object(pk)
        serializer = PlayerStatisticsFullSerializer(player_statistics)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        player_statistics = self.get_object(pk)
        serializer = PlayerStatisticsFullSerializer(player_statistics, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        player_statistics = self.get_object(pk)
        player_statistics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamStatisticsList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        team_statistics_many = TeamStatistics.objects.all()
        serializer = TeamStatisticsFullSerializer(team_statistics_many, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeamStatisticsFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamStatisticsDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return TeamStatistics.objects.get(pk=pk)
        except TeamStatistics.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team_statistics = self.get_object(pk)
        serializer = TeamStatisticsFullSerializer(team_statistics)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        team_statistics = self.get_object(pk)
        serializer = TeamStatisticsFullSerializer(team_statistics, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        team_statistics = self.get_object(pk)
        team_statistics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
