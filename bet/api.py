import requests
from datetime import date

# some sample url
url = 'http://api.football-data.org/v2/competitions/445'
url_teams = "http://api.football-data.org/v2/competitions/445/teams"
url_players = "http://api.football-data.org/v2/teams/57/players"
url_team = "http://api.football-data.org/v2/teams/57"
url_fixtures_for_team = "http://api.football-data.org/v2/teams/57/fixtures/"
url_league_table = "http://api.football-data.org/v2/competitions/445/leagueTable"


def url_conn(url):
    """
    Conntect api server with given url and returns data
    :param url: string - query
    :return: json
    """
    api_key = "1a7d0487f5df473a8357546f6da2385d"  # your key goes here
    headers = {'X-Auth-Token': api_key}
    response = requests.get(url, verify=True, headers=headers)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    return response.json()


def get_competition():
    """
    returns json with competitions, when specifying argument id returns single
    competition with given id in api server,
    sepcifying season returns data for competition from given season
    :param id: int - api server competition id
    :param season: int - year of season start
    :return: json with competition/s data
    """
    url = 'http://api.football-data.org/v2/' \
          'competitions/'
    return url_conn(url)


def get_competitions(id="", season=""):
    """
    returns json with competitions, when specifying argument id returns single
    competition with given id in api server,
    sepcifying season returns data for competition from given season
    :param id: int - api server competition id
    :param season: int - year of season start
    :return: json with competition/s data
    """
    url = 'http://api.football-data.org/v2/' \
          'competitions/{}?season={}'.format(id, season)
    return url_conn(url)


def get_fixtures(competition_id, matchday):
    """
    Returns fixtures for given competition and matchday
    :param competition_id: int - competition id in api server
    :param matchday: int
    :return: json data with fixtures
    """
    url = 'http://api.football-data.org/v2/' \
          'competitions/{}/fixtures?matchday={}'.format(competition_id,
                                                        matchday
                                                        )
    # TODO: Get all fixtures without specifying matchday
    return url_conn(url)


def get_league_table(competition_id, matchday=""):
    """
    Returns league table for competition and given matchday
    :param competition_id: int - competition id in api server
    :return: json data with league table
    """
    url = "http://api.football-data.org/v2/" \
          "competitions/{}/leagueTable?matchday={}".format(competition_id,
                                                           matchday)
    return url_conn(url)


def get_team_last_fixtures(team_api_id):
    """
    Returns last 15 fixtures of given team
    :param team_api_id: int - id of team in api server
    :return: json data with last 15 fixtures of team
    """
    # TODO: Optimize getting last 15 fixtures
    time_frame_stop = date.today().year
    time_frame_start = date.today().year - 1
    url = "http://api.football-data.org/v2/teams/{}/fixtures/?season={}"
    data1 = url_conn(url.format(team_api_id, time_frame_stop))['fixtures']
    data2 = url_conn(url.format(team_api_id, time_frame_start))['fixtures']
    data = data1 + data2
    new_data = []
    for row in data:
        if row['status'] == "FINISHED":
            new_data.append(row)
    return new_data[:15]


# print(get_league_table(394))
# print(get_competitions(id="394"))
# print(get_fixtures(394,1))
# print(get_competitions(season=2016))
print(get_competitions(season=2016))
#print(get_competition())
