from rest_framework import serializers
from main.models import FootballClub, Player, Coach, TeamStatistics, PlayerStatistics, Stadium, Match, Contract, Agent


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('name', 'capacity', 'address')


class StadiumFullSerializer(StadiumSerializer):
    class Meta(StadiumSerializer.Meta):
        fields = StadiumSerializer.Meta.fields + ('openning_date', 'architect',)


class PlayerStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatistics
        fields = ('assists', 'is_injured',)


class PlayerStatisticsFullSerializer(PlayerStatisticsSerializer):
    class Meta(PlayerStatisticsSerializer.Meta):
        fields = PlayerStatisticsSerializer.Meta.fields + ('minutes_played', 'injury_type',)


class TeamStatisticsSerializer(serializers.Serializer):
    matches_played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    loses = serializers.IntegerField()
    points = serializers.IntegerField()
    place = serializers.IntegerField()

    def create(self, validated_data):
        return TeamStatistics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.matches_played = validated_data.get('matches_played', instance.matches_played)
        instance.wins = validated_data.get('wins', instance.wins)
        instance.draws = validated_data.get('draws', instance.draws)
        instance.loses = validated_data.get('loses', instance.loses)
        instance.points = validated_data.get('points', instance.points)
        instance.place = validated_data.get('place', instance.place)
        instance.save()
        return instance



class TeamStatisticsFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamStatistics
        fields = '__all__'


class FootballClubRepresentationSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer()

    class Meta:
        model = FootballClub
        fields = ('title', 'stadium')


class FootballClubFullSerializer(FootballClubRepresentationSerializer):

    statistics = TeamStatisticsSerializer()

    class Meta(FootballClubRepresentationSerializer.Meta):
        fields = FootballClubRepresentationSerializer.Meta.fields + ('website', 'statistics')


class MatchSerializer(serializers.ModelSerializer):
    football_club = FootballClubRepresentationSerializer()
    class Meta:
        model = Match
        fields = ('final_score', 'football_club', 'opponent',)


class MatchFullSerializer(MatchSerializer):
    class Meta(MatchSerializer.Meta):
        fields = MatchSerializer.Meta.fields + ('date', 'weather', 'is_played',)


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('signing_date', 'expiration_date', 'salary',)


class ContractFullSerializer(ContractSerializer):
    class Meta(ContractSerializer.Meta):
        fields = ContractSerializer.Meta.fields + ('previous_club', 'additional_data',)


class AgentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    nationality = serializers.CharField(max_length=50)
    additional_data = serializers.CharField(max_length=500)
    contract_terms = serializers.CharField(max_length=250)

    def create(self, validated_data):
        return Agent.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.additional_data = validated_data.get('additional_data', instance.additional_data)
        instance.contract_terms = validated_data.get('contract_terms', instance.contract_terms)
        instance.save()
        return instance


class PlayerMatchesSerializer(serializers.ModelSerializer):
    statistics = PlayerStatisticsSerializer()
    football_club = FootballClubRepresentationSerializer()
    class Meta:
        model = Player
        fields = ('position', 'height', 'weight', 'football_club', 'statistics',)


class PlayerRepresentationSerializer(serializers.ModelSerializer):
    football_club = FootballClubRepresentationSerializer()
    class Meta:
        model = Player
        fields = ('football_club', 'position', 'shirt_number', 'is_foreign', 'is_from_academy', 'website',)


class PlayerContractSerializer(serializers.ModelSerializer):
    football_club = FootballClubRepresentationSerializer()
    contract = ContractSerializer()
    agent = AgentSerializer()
    class Meta:
        model = Player
        fields = ('football_club', 'contract', 'agent',)


class PlayerFullSerializer(serializers.ModelSerializer):
    football_club = FootballClubRepresentationSerializer()
    contract = ContractSerializer()
    statistics = PlayerStatisticsSerializer()
    agent = AgentSerializer()
    class Meta:
        model = Player
        fields = '__all__'


class CoachSerializer(serializers.ModelSerializer):
    football_club = FootballClubRepresentationSerializer()
    class Meta:
        model = Coach
        fields = ('post', 'football_club',)


class CoachFullSerializer(CoachSerializer):
    contract = ContractSerializer()
    class Meta(CoachSerializer.Meta):
        fields = CoachSerializer.Meta.fields + ('website', 'team_tactics', 'contract',)