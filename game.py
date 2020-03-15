import team
from request import get, _json


class Game:
    def __init__(self, gameID, data):
        self.gameID = gameID
        self.league = data['league']
        self.sport = data['sport']
        self.baseUrl = data['baseUrl']
        self.score = {}
        self.awayTeam = None
        self.homeTeam = None
        self.winProbability = {}
        self.spread = None
        self.overUnder = None
        self.venue = None
        self.attendance = None
        self.broadcast = None

    def getJson(self):
        try:
            return _json('{}/summary?event={}'.format(self.baseUrl, self.gameID))
        except Exception as e:
            print(e)

    def makeGame(self):
        try:
            json = self.getJson()
            teamObjs = json['boxscore']['teams']
            self.awayTeam = team.Team(teamObjs[0]['team']['id'], {
                'league': self.league,
                'sport': self.sport,
                'baseUrl': self.baseUrl,
                'teamNickname': None
            })
            self.homeTeam = team.Team(teamObjs[1]['team']['id'], {
                'league': self.league,
                'sport': self.sport,
                'baseUrl': self.baseUrl,
                'teamNickname': None
            })
            if json['gameInfo']['venue']:
                self.venue = {
                    'name': json['gameInfo']['venue']['fullName'],
                    'city': json['gameInfo']['venue']['address']['city'],
                    'state': json['gameInfo']['venue']['address']['state'],
                    'capacity': json['gameInfo']['venue']['capacity'],
                    'image': (
                        json['gameInfo']['venue']['images'][0]['href'] if json['gameInfo']['venue']['images'] else None)
                }
                self.attendance = (
                    json['gameInfo']['venue']['attendance'] if json['gameInfo']['venue']['attendance'] else None)
                self.broadcast = (json['header']['competitions'][0]['broadcasts'][0]['media']['shortName'] if
                                  json['header']['competitions'][0]['broadcasts'] else None)
            self.getScore()
            self.getGameProbability()
            self.getGameOdds()
        except Exception as e:
            print(e)

    def getTeams(self):
        return {'awayTeam': self.awayTeam, 'homeTeam': self.homeTeam}

    def getScore(self):
        try:
            json = self.getJson()
            if self.score:
                self.score = {}
            if json['scoringPlays']:
                lastScore = json['scoringPlays'][-1]
                self.score = {'awayScore': lastScore['awayScore'], 'homeScore': lastScore['homeScore']}
            return self.score
        except Exception as e:
            print(e)

    def getGameProbability(self):
        try:
            json = self.getJson()
            percentage = None
            winning_team = None
            if json['winprobability']:
                lastProbability = json['winprobability'][-1]
                if lastProbability['homwWinPercentage'] < 0.5:
                    percentage = (1 - int(lastProbability['homeWinPercentage'])) * 100
                    winning_team = self.awayTeam
                else:
                    percentage = int(lastProbability['homeWinPercentage']) * 100
                    winning_team = self.homeTeam
                self.winProbability = {
                    'percentage': percentage,
                    'winningTeam': winningTeam
                }
            return self.winProbability
        except Exception as e:
            print(e)

    def getGameOdds(self):
        try:
            if not self.spread or not self.overUnder:
                json = self.getJson()
                if json['pickcenter']:
                    pickCenter = json['pickcenter'][0]
                    self.spread = pickCenter['details']
                    self.overUnder = pickCenter['overUnder']
            return {
                'spread': self.spread,
                'overUnder': self.overUnder
            }
        except Exception as e:
            print(e)
