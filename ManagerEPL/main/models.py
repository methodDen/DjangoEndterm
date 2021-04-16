from django.db import models

# Create your models here.
class Stadium(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    openning_date = models.DateField(verbose_name='Дата Открытия')
    capacity = models.IntegerField(verbose_name='Вместимость')
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


class PlayerStatistics(Statistics):
    assists = models.IntegerField(verbose_name='Голевые передачи')
    minutes_played = models.IntegerField(verbose_name='Количество сыгранных минут')
    is_injured = models.BooleanField(verbose_name='Травмирован')
    injury_type = models.CharField(max_length=100, verbose_name='Тип трамвы', blank=True, null=True)

    class Meta:
        verbose_name = 'Статистика игрока'
        verbose_name_plural = 'Статистика игроков'


class TeamStatistics(Statistics):
    wins = models.IntegerField(verbose_name='Победы')
    draws = models.IntegerField(verbose_name='Ничьи')
    loses = models.IntegerField(verbose_name='Поражения')
    goals_conceded = models.IntegerField(verbose_name='Пропущенные голы')
    points = models.IntegerField(verbose_name='Количество очков')
    place = models.IntegerField(verbose_name='Место в таблице')

    class Meta:
        verbose_name = 'Статистика клуба'
        verbose_name_plural = 'Статистика клубов'


class FootballClub(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    website = models.CharField(max_length=50, verbose_name='Веб сайт')
    statistics = models.OneToOneField(TeamStatistics, on_delete=models.CASCADE, verbose_name='Статистика команды')
    stadium = models.OneToOneField(Stadium, on_delete=models.CASCADE, verbose_name='Стадион')

    class Meta:
        verbose_name = 'Футбольный клуб'
        verbose_name_plural = 'Футбольные клубы'


class Match(models.Model):
    final_score = models.CharField(max_length=20, verbose_name='Итоговый счет', blank=True, null=True)
    date = models.DateField(verbose_name='Дата')
    weather = models.CharField(max_length=30, verbose_name='Погода', blank=True, null=True)
    opponent = models.CharField(max_length=100, verbose_name='Соперник')
    is_played = models.BooleanField(verbose_name='Завершен')
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='matches', verbose_name='Футбольный клуб')

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'


class Contract(models.Model):
    signing_date = models.DateField(verbose_name='Дата подписания')
    expiration_date = models.DateField(verbose_name='Дата окончания')
    previous_club = models.CharField(max_length=100, verbose_name='Предыдущий клуб', blank=True, null=True)
    salary = models.IntegerField(verbose_name='Зарплата')
    additional_data = models.TextField(max_length=500, verbose_name='Дополнительные сведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    age = models.IntegerField(verbose_name='Возраст')
    nationality = models.CharField(max_length=50, verbose_name='Национальность')
    additional_data = models.TextField(max_length=500, verbose_name='Дополнительные сведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        abstract = True


class Agent(Person):
    contract_terms = models.TextField(max_length=250, verbose_name='Условия контракта')

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'


class Player(Person):
    position = models.CharField(max_length=20, verbose_name='Амплуа')
    height = models.IntegerField(verbose_name='Рост', blank=True, null=True)
    weight = models.IntegerField(verbose_name='Вес', blank=True, null=True)
    shirt_number = models.IntegerField(verbose_name='Номер')
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    is_foreign = models.BooleanField(verbose_name='Легионер')
    is_from_academy = models.BooleanField(verbose_name='Воспитанник клуба')
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='players', verbose_name='Футбольный клуб')
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Контракт')
    statistics = models.OneToOneField(PlayerStatistics, on_delete=models.CASCADE, verbose_name='Статистика игрока')
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, verbose_name='Агент')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Coach(Person):
    post = models.CharField(max_length=50, verbose_name='Пост')
    website = models.CharField(max_length=50, verbose_name='Веб сайт', blank=True, null=True)
    team_tactics = models.CharField(max_length=50, verbose_name='Тактика', blank=True, null=True)
    football_club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='coaches', verbose_name='Футбольный клуб')
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Контракт')

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'

