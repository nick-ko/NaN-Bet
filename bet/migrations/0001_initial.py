# Generated by Django 2.2.3 on 2019-07-31 15:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('bank_account_number', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=128)),
                ('league', models.CharField(max_length=12)),
                ('number_of_matchdays', models.IntegerField()),
                ('year', models.IntegerField()),
                ('number_of_teams', models.IntegerField()),
                ('current_matchday', models.IntegerField()),
                ('api_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('crest_url', models.CharField(blank=True, max_length=256, null=True)),
                ('squad_market_value', models.CharField(blank=True, max_length=64, null=True)),
                ('code', models.CharField(max_length=12, null=True)),
                ('short_name', models.CharField(max_length=64)),
                ('competition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bet.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'SCHEDULED'), (2, 'FINISHED'), (3, 'PLAYING')], default=1)),
                ('matchday', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('goals_home_team', models.IntegerField(blank=True, default=None, null=True)),
                ('goals_away_team', models.IntegerField(blank=True, default=None, null=True)),
                ('course_team_home_win', models.FloatField(blank=True, default=1)),
                ('course_team_away_win', models.FloatField(blank=True, default=1)),
                ('course_draw', models.FloatField(blank=True, default=1)),
                ('fixture_result', models.IntegerField(blank=True, default=-1)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='awayTeam', to='bet.Team')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='competition', to='bet.Competition')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='homeTeam', to='bet.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet_amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('bet', models.IntegerField(choices=[(1, 1), (2, 2), (0, 0)])),
                ('bet_course', models.FloatField(default=0)),
                ('bet_result', models.IntegerField(blank=True, choices=[(0, 'LOST'), (1, 'WON'), (2, 'PENDING')], default=2)),
                ('bet_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bet_user', to='bet.AppUser')),
                ('fixture', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fixture', to='bet.Fixture')),
            ],
        ),
    ]
