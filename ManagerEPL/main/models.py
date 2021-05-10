from django.db import models
from rest_framework import serializers
from utils.validators import validate_size, validate_extension


# Create your models here.

def capacity_range_validation(value):
    if not (1500 <= value <= 150000):
        raise serializers.ValidationError('Inappropriate capacity value')


class Stadium(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    openning_date = models.DateField(verbose_name='Дата Открытия', blank=True, null=True)
    capacity = models.IntegerField(verbose_name='Вместимость', validators=[capacity_range_validation])
    architect = models.CharField(max_length=100, verbose_name='Проектировщик', blank=True, null=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', blank=True, null=True)

    class Meta:
        verbose_name = 'Стадион'
        verbose_name_plural = 'Стадионы'

    def __str__(self):
        return self.name


def validate_matches_played(value):
    if not (1 <= value <= 38):
        raise serializers.ValidationError('Invalid number of matches value')


class Statistics(models.Model):
    matches_played = models.IntegerField(verbose_name='Сыграно матчей', validators=[validate_matches_played])
    yellow_cards = models.IntegerField(verbose_name='Желтые карточки', blank=True, null=True)
    red_cards = models.IntegerField(verbose_name='Красные карточки', blank=True, null=True)
    goals_scored = models.IntegerField(verbose_name='Забитые голы')

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        abstract = True


class PlayerStatisticsManager(models.Manager):  # correct

    def top_goalscorers_stats(self):
        return self.filter(goals_scored__gte=15)

    def top_assistant_stats(self):
        return self.filter(assists__gte=10)


class PlayerStatistics(Statistics):
    assists = models.IntegerField(verbose_name='Голевые передачи', blank=True, null=True)
    minutes_played = models.IntegerField(verbose_name='Количество сыгранных минут', blank=True, null=True)
    is_injured = models.BooleanField(verbose_name='Травмирован')
    injury_type = models.CharField(max_length=100, verbose_name='Тип трамвы', blank=True, null=True)

    objects = PlayerStatisticsManager()

    class Meta:
        verbose_name = 'Статистика игрока'
        verbose_name_plural = 'Статистика игроков'

    def __str__(self):
        return f'Player Statistics {self.id}'


def place_range_validation(value):
    if value > 20 or value < 1:
        raise serializers.ValidationError('Invalid place value')


def validate_wins(value):
    if not (1 <= value <= 38):
        raise serializers.ValidationError('Invalid number of wins value')


def validate_draws(value):
    if not (1 <= value <= 38):
        raise serializers.ValidationError('Invalid number of draws value')


def validate_loses(value):
    if not (1 <= value <= 38):
        raise serializers.ValidationError('Invalid number of loses value')


class TeamStatisticsManager(models.Manager):
    def get_related(self):
        return self.prefetch_related('football_club_set')


class TeamStatistics(Statistics):
    wins = models.IntegerField(verbose_name='Победы', validators=[validate_wins], blank=True, null=True)
    draws = models.IntegerField(verbose_name='Ничьи', validators=[validate_draws], blank=True, null=True)
    loses = models.IntegerField(verbose_name='Поражения', validators=[validate_loses], blank=True, null=True)
    goals_conceded = models.IntegerField(verbose_name='Пропущенные голы', blank=True, null=True)
    points = models.IntegerField(verbose_name='Количество очков')
    place = models.IntegerField(verbose_name='Место в таблице', validators=[place_range_validation, ])
    objects = TeamStatisticsManager()

    class Meta:
        verbose_name = 'Статистика клуба'
        verbose_name_plural = 'Статистика клубов'

    def __str__(self):
        return f'Team Statistics {self.id}'


class FootballClubManager(models.Manager):
    def get_related(self):
        return self.select_related('team_statistics', 'stadium')

    def get_by_place_with_relation(self, place):  # correct
        return self.get_related().filter(team_statistics__place=place)


class FootballClub(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', blank=True, null=True)
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    statistics = models.OneToOneField(TeamStatistics, on_delete=models.CASCADE, verbose_name='Статистика команды',
                                      name='team_statistics', blank=True, null=True)
    stadium = models.OneToOneField(Stadium, on_delete=models.PROTECT, verbose_name='Стадион', blank=True, null=True)
    logo = models.ImageField(upload_to='football_club_photos', validators=[validate_size, validate_extension],
                             null=True, blank=True, verbose_name='Эмблема')

    objects = FootballClubManager()

    class Meta:
        verbose_name = 'Футбольный клуб'
        verbose_name_plural = 'Футбольные клубы'

    def __str__(self):
        return self.title if self.title else f'Unnamed football club {self.id}'


class MatchManager(models.Manager):

    def get_related(self):
        return self.select_related('football_club')

    def get_by_weather(self, weather):  # correct
        return self.get_related().filter(weather=weather)

    def get_by_opponent(self, opponent):  # correct
        return self.filter(opponent=opponent)


def final_score_validation(value):
    if '-' not in value:
        raise serializers.ValidationError('Inappropriate score format')


def weather_validation(value):
    if not (value in ['Sunny', 'Rainy', 'Snow', 'Windy']):
        raise serializers.ValidationError('Inappropriate weather value format')


class Match(models.Model):
    final_score = models.CharField(max_length=20, verbose_name='Итоговый счет', blank=True, null=True,
                                   validators=[final_score_validation])
    date = models.DateField(verbose_name='Дата')
    weather = models.CharField(max_length=30, verbose_name='Погода', blank=True, null=True,
                               validators=[weather_validation])
    opponent = models.CharField(max_length=100, verbose_name='Соперник')
    is_played = models.BooleanField(verbose_name='Завершен')
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='matches',
                                      verbose_name='Футбольный клуб', blank=True, null=True)

    objects = MatchManager()

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

    def __str__(self):
        return f'{self.football_club.title} -- {self.opponent}'


def salary_range_validation(value):
    if value < 500:
        raise serializers.ValidationError('Too small value of salary')


class Contract(models.Model):
    signing_date = models.DateField(verbose_name='Дата подписания')
    expiration_date = models.DateField(verbose_name='Дата окончания')
    previous_club = models.CharField(max_length=100, verbose_name='Предыдущий клуб', blank=True, null=True)
    salary = models.IntegerField(verbose_name='Зарплата', validators=[salary_range_validation])
    additional_data = models.TextField(max_length=500, verbose_name='Дополнительные сведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def __str__(self):
        return f'Contract {self.id}'


def age_range_validation(value):
    if value < 16:
        raise serializers.ValidationError('Inappropriate age value')


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    age = models.IntegerField(verbose_name='Возраст', validators=[age_range_validation], blank=True, null=True)
    nationality = models.CharField(max_length=50, verbose_name='Национальность', blank=True, null=True)
    additional_data = models.TextField(max_length=500, verbose_name='Дополнительные сведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        abstract = True


class AgentManager(models.Manager):  # reverse

    def get_experienced(self):
        return self.filter(age__gte=50)


class Agent(Person):
    contract_terms = models.TextField(max_length=250, verbose_name='Условия контракта')
    photo = models.ImageField(upload_to='agent_photos', validators=[validate_size, validate_extension], null=True,
                              blank=True, verbose_name='Фото')

    objects = AgentManager()

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if (
                    self.first_name and self.last_name) else f'Unnamed agent {self.id}'


class PlayerManager(models.Manager):

    def get_related(self):
        return self.select_related('football_club', 'contract', 'statistics')

    def get_by_football_club_with_relation(self, football_club_id):  # correct
        return self.get_related().filter(football_club_id=football_club_id)

    def get_by_agent_without_relation(self, agent_id):  # correct
        return self.filter(agent_id=agent_id)

    def get_related_statistics(self, player_id):  # Возможно, надо будет передать player_id
        return self.select_related('football_club', 'statistics').filter(pk=player_id)

    def get_players_from_academy(self):  # correct
        return self.filter(is_local=True)

    def get_foreign_players(self):  # correct
        return self.filter(is_foreign=True)

    def get_injured_players(self):  # correct
        return self.get_related().filter(statistics__is_injured=True)  # Player 1-1 Statistics, достаем по statistics

    def get_not_injured_players(self):  # correct
        return self.get_related().filter(statistics__is_injured=False)


def shirt_number_range_validation(value):
    if not (1 <= value <= 99):
        raise serializers.ValidationError('Inappropriate shirt_number value')


def height_range_validation(value):
    if not (150 <= value <= 210):
        raise serializers.ValidationError('Inappropriate height value')


def weight_range_validation(value):
    if not (50 <= value <= 110):
        raise serializers.ValidationError('Inappropriate weight value')


class Player(Person):
    position = models.CharField(max_length=50, verbose_name='Амплуа', blank=True, null=True)
    height = models.IntegerField(verbose_name='Рост', blank=True, null=True, validators=[height_range_validation])
    weight = models.IntegerField(verbose_name='Вес', blank=True, null=True, validators=[weight_range_validation])
    shirt_number = models.IntegerField(verbose_name='Номер', validators=[shirt_number_range_validation], blank=True,
                                       null=True)
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    is_foreign = models.BooleanField(verbose_name='Легионер', blank=True, null=True)
    is_local = models.BooleanField(verbose_name='Воспитанник клуба', blank=True, null=True)

    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='players',
                                      verbose_name='Футбольный клуб', blank=True, null=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Контракт', blank=True, null=True)
    statistics = models.OneToOneField(PlayerStatistics, on_delete=models.CASCADE, verbose_name='Статистика игрока',
                                      blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, verbose_name='Агент', blank=True, null=True)

    objects = PlayerManager()

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if (
                    self.first_name and self.last_name) else f'Unnamed player {self.id}'


class CoachManager(models.Manager):

    def get_related(self):
        return self.select_related('football_club', 'contract')

    def get_by_football_club_with_relation(self, football_club_id):  # correct
        return self.get_related().filter(football_club_id=football_club_id)

    def get_by_football_club_without_relation(self, football_club_id):  # correct
        return self.filter(football_club_id=football_club_id)


def team_tactics_validation(value):
    if value not in ['Super Attack', 'Attack', 'High Possession', 'Defence', 'Super Defence']:
        raise serializers.ValidationError('Inappropriate team_tactics type')


class Coach(Person):
    post = models.CharField(max_length=50, verbose_name='Пост')
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    team_tactics = models.CharField(max_length=50, verbose_name='Тактика', blank=True, null=True,
                                    validators=[team_tactics_validation])
    photo = models.ImageField(upload_to='coach_photos', validators=[validate_size, validate_extension], null=True,
                              blank=True, verbose_name='Фото')
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='coaches',
                                      verbose_name='Футбольный клуб', blank=True, null=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Контракт', blank=True, null=True)

    objects = CoachManager()

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if (
                    self.first_name and self.last_name) else f'Unnamed coach {self.id}'
