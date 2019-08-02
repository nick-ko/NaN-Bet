from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Competition(models.Model):
    caption = models.CharField(max_length=128)
    league = models.CharField(max_length=12)
    number_of_matchdays = models.IntegerField()
    year = models.IntegerField()
    number_of_teams = models.IntegerField()
    current_matchday = models.IntegerField()
    api_id = models.IntegerField()

    def __str__(self):
        return self.caption


class Team(models.Model):
    name = models.CharField(max_length=256)
    crest_url = models.CharField(max_length=256, null=True, blank=True)
    squad_market_value = models.CharField(max_length=64, null=True, blank=True)
    code = models.CharField(max_length=12, null=True)
    short_name = models.CharField(max_length=64)
    competition = models.ForeignKey(Competition, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


STATUS_TAB = ((1, "SCHEDULED"),
              (2, "FINISHED"),
              (3, "PLAYING")
              )

BET_CHOICES = ((1, 1),
               (2, 2),
               (0, 0)
               )


class Fixture(models.Model):
    home_team = models.ForeignKey(Team, related_name='homeTeam', on_delete=models.DO_NOTHING)
    away_team = models.ForeignKey(Team, related_name='awayTeam', on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=STATUS_TAB, default=1)
    matchday = models.IntegerField()
    competition = models.ForeignKey(Competition, related_name='competition', on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    goals_home_team = models.IntegerField(default=None, null=True, blank=True)
    goals_away_team = models.IntegerField(default=None, null=True, blank=True)
    course_team_home_win = models.FloatField(default=1, blank=True)
    course_team_away_win = models.FloatField(default=1, blank=True)
    course_draw = models.FloatField(default=1, blank=True)
    fixture_result = models.IntegerField(default=-1, blank=True)

    def __str__(self):
        return str(self.home_team.name + " - " + self.away_team.name)


class AppUser(models.Model):
    # TODO: change cash to decimal
    cash = models.DecimalField(validators=[MinValueValidator(0.00)],
                               max_digits=6, decimal_places=2)
    bank_account_number = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


class Bet(models.Model):
    BET_RESULTS = ((0, "LOST"),
                   (1, "WON"),
                   (2, "PENDING")
                   )

    bet_user = models.ForeignKey(AppUser, related_name="bet_user", on_delete=models.DO_NOTHING)
    bet_amount = models.DecimalField(validators=[MinValueValidator(0.01)],
                                     max_digits=6, decimal_places=2)
    fixture = models.ForeignKey(Fixture, related_name="fixture", on_delete=models.DO_NOTHING)
    bet = models.IntegerField(choices=BET_CHOICES)
    bet_course = models.FloatField(default=0)
    # bet result 0: LOST, 1: WIN
    bet_result = models.IntegerField(default=2, blank=True, choices=BET_RESULTS)


class Pari(models.Model):
    match = models.CharField(max_length=256)
    home = models.CharField(max_length=256, null=True, blank=True)
    predict = models.CharField(max_length=256, null=True, blank=True)
    montant = models.CharField(max_length=12, null=True)
    cote = models.CharField(max_length=64)
    gain = models.CharField(max_length=64)

    def __str__(self):
        return self.gain


class Betting(models.Model):
    match = models.CharField(max_length=256)
    home = models.CharField(max_length=256, null=True, blank=True)
    predict = models.CharField(max_length=256, null=True, blank=True)
    montant = models.DecimalField(validators=[MinValueValidator(0.01)],
                                  max_digits=6, decimal_places=2)
    cote = models.DecimalField(validators=[MinValueValidator(0.01)],
                               max_digits=6, decimal_places=2)
    gain = models.DecimalField(validators=[MinValueValidator(0.01)],
                               max_digits=6, decimal_places=2)

    def __str__(self):
        return self.gain
