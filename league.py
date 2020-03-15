import team
import game
import player
import conference
from request import get, _json


class League:
    def __init__(self, leagueName, data):
        self.league = leagueName
        self.sport = data['sport']
        self.baseUrl = data['baseUrl']
        self.teams = []
        self.conferences = []
        self.rankings = {}
        self.currentGames = []

    def Team(self, ID):
        try:
            json = _json('{}/teams/{}'.format(self.baseUrl, ID.lower()))
            new_team = None
            if ID.isnumeric():
                new_team = team.Team(ID, {
                    'teamNickname': None,
                    'league': self.league,
                    'sport': self.sport,
                    'baseUrl': self.baseUrl
                })
            else:
                new_team = team.Team(self.getTeamIDFromName(ID.lower()), {
                    'teamNickname': None,
                    'league': self.league,
                    'sport': self.sport,
                    'baseUrl': self.baseUrl
                })
            return new_team
        except Exception as e:
            print(e)

    def getTeamIDFromName(self, keyword):
        json = _json('{}/teams/{}'.format(self.baseUrl, keyword.lower()))
        return json['teamInfo']['team']['id']

    def Conference(self, ID):
        try:
            new_conference = conference.Conference(ID, {
                'league': self.league,
                'sport': self.sport,
                'baseUrl': self.baseUrl
            })
            return new_conference
        except Exception as e:
            print(e)

    def Game(self, ID):
        try:
            new_game = game.Game(ID, {
                'league': self.league,
                'sport': self.sport,
                'baseUrl': self.baseUrl
            })
            return new_game
        except Exception as e:
            print(e)

    def Player(self, ID):
        try:
            new_player = player.Player(ID, {
                'league': self.league,
                'sport': self.sport,
                'baseUrl': 'https://site.web.api.espn.com/apis/common/v3/sports/{}/{}/athletes'.format(self.sport,
                                                                                                       self.league)
            })
            return new_player
        except Exception as e:
            print(e)

    def getTeams(self):
        try:
            if not self.teams:
                json = _json('{}/teams?limit=1000'.format(self.baseUrl))
                for this_team in json['sports'][0]['leagues'][0]['teams']:
                    self.teams.append(
                        team.Team(this_team['team']['id'], {
                            'league': self.league,
                            'sport': self.sport,
                            'baseUrl': self.baseUrl,
                            'teamNickname': None
                        })
                    )
            return self.teams
        except Exception as e:
            print(e)

    def getRankings(self):
        try:
            json = _json('{}/rankings'.format(self.baseUrl))
            self.rankings = json
            return self.rankings
        except Exception as e:
            print(e)

    def getNews(self):
        try:
            json = _json('{}/news'.format(self.baseUrl))
            return json
        except Exception as e:
            print(e)

    def getCurrentGames(self):
        try:
            self.currentGames = []
            json = _json('{}/scoreboard'.format(self.baseUrl))
            for this_game in json['events']:
                new_game = game.Game(this_game['id'], {
                    'league': self.league,
                    'sport': self.sport,
                    'baseUrl': self.baseUrl
                })
                self.currentGames.append(new_game)
            return self.currentGames
        except Exception as e:
            print(e)
