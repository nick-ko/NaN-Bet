import http.client
import json
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests
from decimal import Decimal
import urllib.request
from urllib.request import urlopen

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import Betting


def index(request):
    response = requests.get(
        'http://livescore-api.com/api-client/scores/live.json?key=SsvL3L7U1muJsdZZ&secret=ezE8NxS9Q0uMNJdGbIrfuz9vWEfoReo6')
    response.json()
    data = response.json()
    match = data['data']['match']

    match_data = []
    index = 0
    while index < len(match):
        live_match = {
            'score': data['data']['match'][index]['score'],
            'competition_name': data['data']['match'][index]['competition_name'],
            'home_name': data['data']['match'][index]['home_name'],
            'away_name': data['data']['match'][index]['away_name'],
            'status': data['data']['match'][index]['status'],
            'time': data['data']['match'][index]['time'],
        }
        match_data.append(live_match)
        index += 1
    context = {'match_data': match_data}
    # print(context)
    return render(request, 'pages/index.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Vous etez connectez')
            return redirect('dashboard')
        else:
            messages.error(request, 'Speudo ou Mot de passe Incorrect')
            return redirect('login')

    else:
        return render(request, 'pages/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Vous vous etez deconnecter')
        return redirect('index')


def signin(request):
    if request.method == 'POST':
        # Get value
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if password == c_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Cet email existe deja')
                return redirect('register')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Cet speudo existe deja')
                    return redirect('register')
                else:
                    # Everything is good
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    # loging after register
                    # auth.login(request, user)
                    # messages.success(request, 'Vous etez connectez')
                    user.save()
                    messages.success(request, 'Vous vous etez inscrit ')
                    return redirect('login')
        else:
            messages.error(request, 'les mot de passe ne concorde pas')
            return redirect('register')
    else:
        return render(request, 'pages/signin.html')


def profil(request):
    return render(request, 'pages/profil.html')


def dashboard(request):
    if request.method == 'POST':
        match = request.POST['match']
        home = request.POST['home']
        away = request.POST['away']
        choix = request.POST['choix']

        bet = []
        bet_data = {
            'match': match,
            'home': home,
            'away': away,
            'choix': choix
        }
        bet.append(bet_data)
        context = {'bet_data': bet_data}
        messages.success(request, 'Parie effectuer avec success veuiller confirmer')
        return render(request, 'pages/account.html', context)

    response = requests.get(
        'http://livescore-api.com/api-client/fixtures/matches.json?key=SsvL3L7U1muJsdZZ&secret=ezE8NxS9Q0uMNJdGbIrfuz9vWEfoReo6')
    response.json()
    data = response.json()
    match = data['data']['fixtures']

    next_data = []
    index = 0
    while index < len(match):
        next_match = {
            'round': data['data']['fixtures'][index]['round'],
            'location': data['data']['fixtures'][index]['location'],
            'home_name': data['data']['fixtures'][index]['home_name'],
            'home_id': int(data['data']['fixtures'][index]['home_id']) / 1000,
            'away_name': data['data']['fixtures'][index]['away_name'],
            'away_id': int(data['data']['fixtures'][index]['away_id']) / 1000,
            'time': data['data']['fixtures'][index]['time'],
            'date': data['data']['fixtures'][index]['date'],
        }
        next_data.append(next_match)
        index += 1

    response = requests.get(
        'http://livescore-api.com/api-client/scores/live.json?key=SsvL3L7U1muJsdZZ&secret=ezE8NxS9Q0uMNJdGbIrfuz9vWEfoReo6')
    response.json()
    data = response.json()
    match = data['data']['match']

    live_data = []
    index = 0
    while index < len(match):
        live_match = {
            'score': data['data']['match'][index]['score'],
            'competition_name': data['data']['match'][index]['competition_name'],
            'home_name': data['data']['match'][index]['home_name'],
            'home_id': int(data['data']['match'][index]['home_id']) / 1000,
            'away_name': data['data']['match'][index]['away_name'],
            'away_id': int(data['data']['match'][index]['away_id']) / 1000,
            'status': data['data']['match'][index]['status'],
            'time': data['data']['match'][index]['time'],
        }
        live_data.append(live_match)
        index += 1

    req = requests.get(
        'http://livescore-api.com/api-client/scores/history.json?key=SsvL3L7U1muJsdZZ&secret=ezE8NxS9Q0uMNJdGbIrfuz9vWEfoReo6')
    req.json()
    data = req.json()
    history = data['data']['match']

    history_data = []
    index = 0
    while index < len(history):
        history_match = {
            'score': data['data']['match'][index]['score'],
            'ht_score': data['data']['match'][index]['ht_score'],
            'home_name': data['data']['match'][index]['home_name'],
            'home_id': int(data['data']['match'][index]['home_id']) / 1000,
            'away_name': data['data']['match'][index]['away_name'],
            'away_id': int(data['data']['match'][index]['away_id']) / 1000,
            'competition_name': data['data']['match'][index]['competition_name'],
            'date': data['data']['match'][index]['date'],
        }
        history_data.append(history_match)
        index += 1

    context = {'next_data': next_data, 'live_data': live_data, 'history_data': history_data}
    print(context)
    return render(request, 'pages/dashboard.html', context)


def account(request):
    betting = Betting.objects.all()
    context={
        'betting':betting
    }
    if request.method == 'POST':
        match = request.POST['match']
        predict = request.POST['predict']
        cote = Decimal(request.POST['cote'])
        montant = Decimal(request.POST['montant'])
        gain = cote * montant

        bet = Betting(match=match, predict=predict, montant=montant, cote=cote, gain=gain)
        bet.save()
        messages.success(request, 'Pari validé')
    return render(request, 'pages/account.html', context)
