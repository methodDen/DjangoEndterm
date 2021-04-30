from rest_framework import serializers
from main.models import FootballClub, Player, Coach, TeamStatistics, PlayerStatistics, Stadium, Match, Contract, Agent


class StadiumSerializer(serializers.ModelSerializer):

    def validate_capacity(self, value):
        if not (500 <= value <= 150000):
            raise serializers.ValidationError('Inappropriate capacity value')
        return value

    class Meta:
        model = Stadium
        fields = ('name', 'capacity', 'address')


class StadiumFullSerializer(StadiumSerializer):
    class Meta(StadiumSerializer.Meta):
        fields = StadiumSerializer.Meta.fields + ('openning_date', 'architect',)


class PlayerStatisticsSerializer(serializers.ModelSerializer):
    def validate_matches_played(self, value):
        if not (1 <= value <= 38):
            raise serializers.ValidationError('Invalid number of matches value')
        return value

    class Meta:
        model = PlayerStatistics
        fields = ('matches_played', 'goals_scored', 'assists', 'yellow_cards', 'red_cards', 'is_injured',)


class PlayerStatisticsFullSerializer(PlayerStatisticsSerializer):
    class Meta(PlayerStatisticsSerializer.Meta):
        fields = PlayerStatisticsSerializer.Meta.fields + ('minutes_played', 'injury_type',)


class TeamStatisticsSerializer(serializers.Serializer):  # experimental
    matches_played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    loses = serializers.IntegerField()
    goals_scored = serializers.IntegerField()
    goals_conceded = serializers.IntegerField()
    yellow_cards = serializers.IntegerField()
    red_cards = serializers.IntegerField()
    points = serializers.IntegerField()
    place = serializers.IntegerField()

    def validate_matches_played(self, value):
        if not (1 <= value <= 38):
            raise serializers.ValidationError('Invalid number of matches value')
        return value

    def validate_wins(self, value):
        if not (1 <= value <= 38):
            raise serializers.ValidationError('Invalid number of wins value')
        return value

    def validate_draws(self, value):
        if not (1 <= value <= 38):
            raise serializers.ValidationError('Invalid number of draws value')
        return value

    def validate_loses(self, value):
        if not (1 <= value <= 38):
            raise serializers.ValidationError('Invalid number of loses value')
        return value

    def validate_place(self, value):
        if value > 20 or value < 1:
            raise serializers.ValidationError('Invalid place value')
        return value

    def create(self, validated_data):
        return TeamStatistics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.matches_played = validated_data.get('matches_played', instance.matches_played)
        instance.wins = validated_data.get('wins', instance.wins)
        instance.draws = validated_data.get('draws', instance.draws)
        instance.loses = validated_data.get('loses', instance.loses)
        instance.goals_scored = validated_data.get('goals_scored', instance.goals_scored)
        instance.goals_conceded = validated_data.get('goals_conceded', instance.goals_conceded)
        instance.yellow_cards = validated_data.get('yellow_cards', instance.yellow_cards)
        instance.red_cards = validated_data.get('red_cards', instance.red_cards)
        instance.points = validated_data.get('points', instance.points)
        instance.place = validated_data.get('place', instance.place)
        instance.save()
        return instance


class TeamStatisticsFullSerializer(serializers.ModelSerializer):  # Нужно ли?
    class Meta:
        model = TeamStatistics
        fields = '__all__'


class FootballClubSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballClub
        fields = ('title',)


class FootballClubRepresentationSerializer(FootballClubSimpleSerializer):
    stadium = StadiumSerializer()
    team_statistics = TeamStatisticsSerializer()

    class Meta(FootballClubSimpleSerializer.Meta):
        fields = FootballClubSimpleSerializer.Meta.fields + ('stadium', 'team_statistics',)


class FootballClubFullSerializer(FootballClubRepresentationSerializer):
    class Meta(FootballClubRepresentationSerializer.Meta):
        fields = FootballClubRepresentationSerializer.Meta.fields + ('website', 'team_statistics')

class MatchSeparateSerializer(serializers.ModelSerializer):
    def validate_final_score(self, value):
        if '-' not in value:
            raise serializers.ValidationError('Inappropriate final score format')
        return value

    class Meta:
        model = Match
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):

    def validate_final_score(self, value):
        if '-' not in value:
            raise serializers.ValidationError('Inappropriate final score format')
        return value

    football_club = FootballClubSimpleSerializer()

    class Meta:
        model = Match
        fields = ('final_score', 'football_club', 'opponent',)


class MatchFullSerializer(MatchSerializer):
    class Meta(MatchSerializer.Meta):
        fields = MatchSerializer.Meta.fields + ('date', 'weather', 'is_played',)

    def validate_weather(self, value):
        if value not in ['Sunny', 'Rainy', 'Snow', 'Windy']:
            raise serializers.ValidationError('Inappropriate weather format')
        return value

    def update(self, instance, validated_data):
        instance.final_score = validated_data.get('final_score', instance.final_score)
        instance.date = validated_data.get('date', instance.date)
        instance.weather = validated_data.get('weather', instance.weather)
        instance.opponent = validated_data.get('opponent', instance.opponent)
        instance.is_played = validated_data.get('is_played', instance.is_played)
        instance.save()
        return instance


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('signing_date', 'expiration_date', 'salary',)

    def validate_salary(self, value):
        if value < 500:
            raise serializers.ValidationError('Too small value of salary')
        return value


class ContractFullSerializer(ContractSerializer):
    class Meta(ContractSerializer.Meta):
        fields = ContractSerializer.Meta.fields + ('previous_club', 'additional_data',)


class AgentSerializer(serializers.Serializer):  # experimental
    def validate_age(self, value):
        if value < 16:
            raise serializers.ValidationError('Inappropriate age value')
        return value

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
    football_club = FootballClubSimpleSerializer()

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'age', 'nationality',
                  'position', 'football_club', 'statistics')


class PlayerRepresentationSerializer(serializers.ModelSerializer):
    football_club = FootballClubRepresentationSerializer()

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'age', 'nationality', 'position',
                  'football_club', 'shirt_number', 'is_foreign', 'is_local', 'website',)


class PlayerContractSerializer(serializers.ModelSerializer):  # experimental
    football_club = FootballClubSimpleSerializer()
    contract = ContractSerializer()
    agent = AgentSerializer()

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'age', 'nationality',
                  'football_club', 'contract', 'agent',)


class PlayerFullSerializer(serializers.Serializer):

    def validate_age(self, value):
        if value < 16 or value > 40:
            raise serializers.ValidationError('Inappropriate age value')
        return value

    def validate_shirt_number(self, value):
        if not (1 <= value <= 99):
            raise serializers.ValidationError('Inappropriate shirt_number value')
        return value

    def validate_height(self, value):
        if not (150 <= value <= 210):
            raise serializers.ValidationError('Inappropriate height value')
        return value

    def validate_weight(self, value):
        if not (50 <= value <= 110):
            raise serializers.ValidationError('Inappropriate weight value')
        return value

    def validate_position(self, value):
        position_list = ['Left winger', 'Right winger', 'Centre forward', 'Striker', 'Centre midfielder',
                         'Defensive midfielder',
                         'Attacking midfielder', 'Left midfielder', 'Right midfielder', 'Centre back', 'Right fullback',
                         'Left fullback', 'Right wingback', 'Left wingback', 'Goalkeeper']
        if value not in position_list:
            raise serializers.ValidationError(f'Inappropriate position value. Choose from {[position_list]}')
        return value

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    nationality = serializers.CharField(max_length=50)
    additional_data = serializers.CharField(max_length=500)
    position = serializers.CharField(max_length=50)
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    shirt_number = serializers.IntegerField()
    website = serializers.CharField(max_length=50)
    is_foreign = serializers.BooleanField()
    is_local = serializers.BooleanField()
    football_club = FootballClubRepresentationSerializer()
    contract = ContractSerializer()
    statistics = PlayerStatisticsSerializer()
    agent = AgentSerializer()

    def create(self, validated_data):
        stadium_data = validated_data['football_club'].pop('stadium')
        team_statistics_data = validated_data['football_club'].pop('team_statistics')
        stadium = Stadium.objects.create(**stadium_data)
        team_statistics = TeamStatistics.objects.create(**team_statistics_data)
        football_club_data = validated_data.pop('football_club')
        fc = FootballClub.objects.create(stadium=stadium, team_statistics=team_statistics, **football_club_data)
        contract_data = validated_data.pop('contract')
        contract = Contract.objects.create(**contract_data)
        agent_data = validated_data.pop('agent')
        agent = Agent.objects.create(**agent_data)
        statistics_data = validated_data.pop('statistics')
        statistics = PlayerStatistics.objects.create(**statistics_data)
        player = Player.objects.create(football_club=fc, contract=contract, agent=agent, statistics=statistics,
                                       **validated_data)
        return player

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.additional_data = validated_data.get('additional_data', instance.additional_data)
        instance.position = validated_data.get('position', instance.position)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.shirt_number = validated_data.get('shirt_number', instance.shirt_number)
        instance.website = validated_data.get('website', instance.website)
        instance.is_foreign = validated_data.get('is_foreign', instance.is_foreign)
        instance.is_local = validated_data.get('is_local', instance.is_local)
        stadium_data = validated_data['football_club'].pop('stadium')
        team_statistics_data = validated_data['football_club'].pop('team_statistics')
        football_club_data = validated_data.pop('football_club')
        football_club = instance.football_club
        football_club.title = football_club_data.get('title', football_club.title)
        football_club.save()
        stadium = football_club.stadium
        stadium.name = stadium_data.get('name', stadium.name)
        stadium.capacity = stadium_data.get('capacity', stadium.capacity)
        stadium.address = stadium_data.get('address', stadium.address)
        stadium.save()
        contract_data = validated_data.pop('contract')
        contract = instance.contract
        contract.signing_date = contract_data.get('signing_date', contract.signing_date)
        contract.expiration_date = contract_data.get('expiration_date', contract.expiration_date)
        contract.salary = contract_data.get('salary', contract.salary)
        contract.save()
        statistics_data = validated_data.pop('statistics')
        statistics = instance.statistics
        statistics.matches_played = statistics_data.get('matches_played', statistics.matches_played)
        statistics.goals_scored = statistics_data.get('goals_scored', statistics.goals_scored)
        statistics.assists = statistics_data.get('assists', statistics.assists)
        statistics.yellow_cards = statistics_data.get('yellow_cards', statistics.yellow_cards)
        statistics.red_cards = statistics_data.get('red_cards', statistics.red_cards)
        statistics.is_injured = statistics_data.get('is_injured', statistics.is_injured)
        statistics.save()
        agent_data = validated_data.pop('agent')
        agent = instance.agent
        agent.first_name = agent_data.get('first_name', agent.first_name)
        agent.last_name = agent_data.get('last_name', agent.last_name)
        agent.age = agent_data.get('age', agent.age)
        agent.nationality = agent_data.get('nationality', agent.nationality)
        agent.additional_data = agent_data.get('additional_data', agent.additional_data)
        agent.contract_terms = agent_data.get('contract_terms', agent.contract_terms)
        agent.save()
        team_statistics = football_club.team_statistics
        team_statistics.matches_played = team_statistics_data.get('matches_played', team_statistics.matches_played)
        team_statistics.goals_scored = team_statistics_data.get('goals_scored', team_statistics.goals_scored)
        team_statistics.yellow_cards = team_statistics_data.get('yellow_cards', team_statistics.yellow_cards)
        team_statistics.red_cards = team_statistics_data.get('red_cards', team_statistics.red_cards)
        team_statistics.place = team_statistics_data.get('place', team_statistics.place)
        team_statistics.wins = team_statistics_data.get('wins', team_statistics.wins)
        team_statistics.draws = team_statistics_data.get('draws', team_statistics.draws)
        team_statistics.loses = team_statistics_data.get('loses', team_statistics.loses)
        team_statistics.goals_conceded = team_statistics_data.get('goals_conceded', team_statistics.goals_conceded)
        team_statistics.points = team_statistics_data.get('points', team_statistics.points)
        team_statistics.place = team_statistics_data.get('place', team_statistics.place)
        team_statistics.save()
        instance.save()
        return instance


class CoachSerializer(serializers.ModelSerializer):
    def validate_team_tactics(self, value):
        if value not in ['Super Attack', 'Attack', 'High Possession', 'Defence', 'Super Defence']:
            raise serializers.ValidationError('Inappropriate team_tactics type')
        return value

    football_club = FootballClubSimpleSerializer()

    class Meta:
        model = Coach
        fields = ('first_name', 'last_name', 'age', 'nationality', 'football_club', 'post',)


class CoachFullSerializer(CoachSerializer):
    contract = ContractSerializer()

    class Meta(CoachSerializer.Meta):
        fields = CoachSerializer.Meta.fields + ('website', 'team_tactics', 'contract',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.post = validated_data.get('post', instance.post)
        instance.website = validated_data.get('website', instance.website)
        instance.team_tactics = validated_data.get('team_tactics', instance.team_tactics)
        instance.save()
        return instance
