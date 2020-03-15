import team
from request import get, _json


class Player:
    def __init__(self, playerID, data):
        self.playerID = playerID
        self.firstName = None
        self.lastName = None
        self.league = data['league']
        self.sport = data['sport']
        self.baseUrl = data['baseUrl']
        self.team = None
        self.position = None
        self.jerseyNumber = None

    def getJson(self):
        try:
            return _json('{}/{}'.format(self.baseUrl, self.playerID))
        except Exception as e:
            print(e)

    def updatePlayerInfo(self):
        try:
            json = self.getJson()
            if json['athlete']:
                json = json['athlete']
            try:
                self.firstName = json['firstName']
                self.lastName = json['lastName']
                self.jerseyNumber = json['jersey']
                if json['position']:
                    self.position = json['position']['abbreviation']
                if json['team']:
                    self.team = team.Team(json['team']['id'], {
                        'teamNickname': None,
                        'league': self.league,
                        'sport': self.sport,
                        'baseUrl': 'http://site.api.espn.com/apis/site/v2/sports/{}/{}'.format(self.sport, self.league)
                    })
            except Exception as e:
                print('Error in inner try: {}'.format(e))
                pass
        except Exception as e:
            print('Error in outer try: {}'.format(e))

    def getPlayerTeam(self):
        return self.team

    def getPlayerStatsSummary(self):
        json = self.getJson()
        if 'athlete' in json:
            if 'statsSummary' in json['athlete']:
                return json['athlete']['statsSummary']

    def getPlayerFullStats(self):
        if self.league:
            json = _json('{}/{}/splits'.format(self.baseUrl, self.playerID))
            return json
        json = _json('{}/{}/statisticslog'.format(self.baseUrl, self.playerID))
        if 'entries' in json:
            return json['entries']
