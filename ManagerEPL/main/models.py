from django.db import models
from rest_framework import serializers


# Create your models here.

def capacity_range_validation(value):
    if not (1500 <= value <= 150000):
        raise serializers.ValidationError('Inappropriate capacity value')

class Stadium(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    openning_date = models.DateField(verbose_name='Дата Открытия')
    capacity = models.IntegerField(verbose_name='Вместимость',validators=[capacity_range_validation])
    architect = models.CharField(max_length=100, verbose_name='Проектировщик', blank=True, null=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', blank=True, null=True)

    class Meta:
        verbose_name = 'Стадион'
        verbose_name_plural = 'Стадионы'


class Statistics(models.Model):
    matches_played = models.IntegerField(verbose_name='Сыграно матчей')
    yellow_cards = models.IntegerField(verbose_name='Желтые карточки')
    red_cards = models.IntegerField(verbose_name='Красные карточки')
    goals_scored = models.IntegerField(verbose_name='Забитые голы')

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        abstract = True


class PlayerStatisticsManager(models.Manager): #correct

    def get_by_player(self, player_id):
        # p = Player.objects.get(id=player_id)
        return self.filter(id=player_id) #?


class PlayerStatistics(Statistics):
    assists = models.IntegerField(verbose_name='Голевые передачи')
    minutes_played = models.IntegerField(verbose_name='Количество сыгранных минут')
    is_injured = models.BooleanField(verbose_name='Травмирован')
    injury_type = models.CharField(max_length=100, verbose_name='Тип трамвы', blank=True, null=True)

    objects = PlayerStatisticsManager()

    class Meta:
        verbose_name = 'Статистика игрока'
        verbose_name_plural = 'Статистика игроков'


def place_range_validation(value):
    if not (1 <= value <= 20):
        raise serializers.ValidationError('Invalid place value')


class TeamStatistics(Statistics):
    wins = models.IntegerField(verbose_name='Победы')
    draws = models.IntegerField(verbose_name='Ничьи')
    loses = models.IntegerField(verbose_name='Поражения')
    goals_conceded = models.IntegerField(verbose_name='Пропущенные голы')
    points = models.IntegerField(verbose_name='Количество очков')
    place = models.IntegerField(verbose_name='Место в таблице', validators=[place_range_validation])

    class Meta:
        verbose_name = 'Статистика клуба'
        verbose_name_plural = 'Статистика клубов'


class FootballClubManager(models.Manager):
    def get_related(self):
        return self.select_related('statistics', 'stadium')

    def get_by_place_with_relation(self, place): #correct
        return self.get_related().filter(statistics__place=place)


class FootballClub(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    website = models.CharField(max_length=50, verbose_name='Веб сайт')
    statistics = models.OneToOneField(TeamStatistics, on_delete=models.CASCADE, verbose_name='Статистика команды')
    stadium = models.OneToOneField(Stadium, on_delete=models.CASCADE, verbose_name='Стадион')

    objects = FootballClubManager()

    class Meta:
        verbose_name = 'Футбольный клуб'
        verbose_name_plural = 'Футбольные клубы'


class MatchManager(models.Manager):

    def get_related(self):
        return self.select_related('football_club')

    def get_by_football_club_with_relation(self, football_club_id): #correct
        return self.get_related().filter(id=football_club_id)

    def get_by_opponent(self, opponent): #correct
        return self.filter(opponent=opponent)


def final_score_validation(value):
    if '-' not in value:
        raise serializers.ValidationError('Inappropriate score format')

def weather_validation(value):
    if not (value in ['Sunny', 'sunny', 'Rainy', 'rainy', 'Snow', 'snow', 'Windy', 'windy']):
        raise serializers.ValidationError('Inappropriate weather value format' )


class Match(models.Model):
    final_score = models.CharField(max_length=20, verbose_name='Итоговый счет', blank=True, null=True, validators=[final_score_validation])
    date = models.DateField(verbose_name='Дата')
    weather = models.CharField(max_length=30, verbose_name='Погода', blank=True, null=True, validators=[weather_validation])
    opponent = models.CharField(max_length=100, verbose_name='Соперник')
    is_played = models.BooleanField(verbose_name='Завершен')
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='matches',
                                      verbose_name='Футбольный клуб')

    objects = MatchManager()

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'


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

def age_range_validation(value):
    if value < 16:
        raise serializers.ValidationError('Inappropriate age value')

class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    age = models.IntegerField(verbose_name='Возраст', validators=[age_range_validation])
    nationality = models.CharField(max_length=50, verbose_name='Национальность')
    additional_data = models.TextField(max_length=500, verbose_name='Дополнительные сведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        abstract = True


class AgentManager(models.Manager): #reverse

    def get_related(self):
        return self.prefetch_related('player_set')

    def get_by_player(self, player_id):

        return self.get_related().filter(id=player_id)


class Agent(Person):
    contract_terms = models.TextField(max_length=250, verbose_name='Условия контракта')
    objects = AgentManager()
    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'


class PlayerManager(models.Manager):

    def get_related(self):
        return self.select_related('football_club', 'contract', 'statistics')

    def get_by_football_club_with_relation(self, football_club_id): # correct
        return self.get_related().filter(football_club_id=football_club_id)

    def get_by_agent_without_relation(self, agent_id): #correct
        return self.filter(agent_id=agent_id)

    def get_players_from_academy(self): #correct
        return self.filter(is_from_academy=True)

    def get_foreign_players(self): #correct
        return self.filter(is_foreign=True)

    def get_by_position_without_relation(self, position): #correct
        return self.filter(position=position)

    def get_by_position_with_relation(self, position): #correct
        return self.get_related().filter(position=position)

    def get_injured_players(self): #correct
        return self.get_related().filter(statistics__is_injured=True) # Player 1-1 Statistics, достаем по statistics

    def get_not_injured_players(self): #correct
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
    position = models.CharField(max_length=50, verbose_name='Амплуа')
    height = models.IntegerField(verbose_name='Рост', blank=True, null=True, validators=[height_range_validation])
    weight = models.IntegerField(verbose_name='Вес', blank=True, null=True, validators=[weight_range_validation])
    shirt_number = models.IntegerField(verbose_name='Номер', validators=[shirt_number_range_validation])
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    is_foreign = models.BooleanField(verbose_name='Легионер')
    is_from_academy = models.BooleanField(verbose_name='Воспитанник клуба')
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='players',
                                      verbose_name='Футбольный клуб')
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Контракт')
    statistics = models.OneToOneField(PlayerStatistics, on_delete=models.CASCADE, verbose_name='Статистика игрока')
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, verbose_name='Агент')

    objects = PlayerManager()

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class CoachManager(models.Manager):

    def get_related(self):
        return self.select_related('football_club', 'contract')

    def get_by_football_club_with_relation(self, football_club_id): # correct
        return self.get_related().filter(football_club_id=football_club_id)

    def get_by_football_club_without_relation(self, football_club_id): # correct
        return self.filter(football_club_id=football_club_id)


def team_tactics_validation(value):
    if value not in ['Все в атаку', 'Атакующая', 'Высокое владение', 'Защитная', 'Глухая оборона']:
        raise serializers.ValidationError('Inappropriate team_tactics type')

class Coach(Person):
    post = models.CharField(max_length=50, verbose_name='Пост')
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    team_tactics = models.CharField(max_length=50, verbose_name='Тактика', blank=True, null=True, validators=[team_tactics_validation])
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='coaches',
                                      verbose_name='Футбольный клуб')
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Контракт')
    objects = CoachManager()
    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'
