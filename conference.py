import team
from request import get, _json


class Conference:
    def __init__(self, conferenceID, data):
        self.conferenceID = conferenceID
        self.league = data['league']
        self.sport = data['sport']
        self.baseUrl = data['baseUrl']
        self.name = None
        self.teams = []

    def getTeams(self):
        try:
            if not self.teams:
                self.teams = []
                json = _json('{}/teams?groups={}&limit=1000'.format(self.baseUrl, self.conferenceID))
                for this_team in json['sports'][0]['leagues'][0]['teams']:
                    new_team = team.Team(this_team['team']['id'], {
                        'league': self.league,
                        'sport': self.sport,
                        'baseUrl': self.baseUrl,
                        'teamNickname': None
                    })
                    self.teams.append(new_team)
            return self.teams
        except Exception as e:
            print(e)
