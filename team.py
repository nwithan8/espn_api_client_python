import game
import player
import conference
from request import get, _json


class Team:
    def __init__(self, teamID, data):
        self.teamID = teamID
        self.league = data['league']
        self.sport = data['sport']
        self.baseUrl = data['baseUrl']
        self.nickname = (data['teamNickname'] if data['teamNickname'] else None)
        self.abbreviation = None
        self.location = None
        self.mascot = None
        self.displayName = None
        self.color = None
        self.teamLogoURL = None
        self.conference = None
        self.links = {}
        self.schedule = []
        self.statistics = {}
        self.record = {}
        self.roster = []

    def getTeamIDFromName(self, keyword):
        json = _json('{}/teams/{}'.format(self.baseUrl, keyword.lower()))
        self.teamID = json['teamInfo']['team']['id']
        return self.teamID

    def getJson(self):
        try:
            return _json('{}/teams/{}'.format(self.baseUrl, self.teamID))
        except Exception as e:
            print(e)

    def makeTeam(self):
        try:
            json = self.getJson()
            if json['team']:
                self.nickname = json['team']['nickname']
                self.abbreviation = json['team']['abbreviation']
                self.location = json['team']['location']
                self.mascot = json['team']['name']
                self.displayName = json['team']['displayName']
                self.color = json['team']['color']
                self.teamLogoURL = json['team']['logos'][0]['href']
                self.record = {
                    'wins': json['team']['record']['items'][0]['stats'][1]['value'],
                    'losses': json['team']['record']['items'][0]['stats'][2]['value'],
                    'ties': json['team']['record']['items'][0]['stats'][5]['value']
                }
                self.statistics = json['team']['record']['items']
                self.links = json['team']['links']
                self.getTeamSchedule()
                self.getTeamConference()
                self.getTeamRoster()
        except Exception as e:
            print(e)

    def getTeamSchedule(self):
        try:
            if not self.schedule:
                json = _json('{}/teams/{}/schedule'.format(self.baseUrl, self.teamID))
                sched = []
                for this_game in json['events']:
                    new_game = game.Game(this_game['id'], {
                        'league': self.league,
                        'sport': self.sport,
                        'baseUrl': self.baseUrl
                    })
                    sched.append(new_game)
                self.schedule = sched
            return self.schedule
        except Exception as e:
            print(e)

    def getTeamConference(self):
        try:
            if not self.conference:
                json = self.getJson()
                self.conference = conference.Conference(json['team']['groups']['parent']['id'], {
                    'league': self.league,
                    'sport': self.sport,
                    'baseUrl': self.baseUrl
                })
            return self.conference
        except Exception as e:
            print(e)

    def getTeamRoster(self):
        try:
            if not self.roster:
                json = _json('{}/teams/{}/roster'.format(self.baseUrl, self.teamID))
                rost = []
                for this_group in json['athletes']:
                    dictionary = {'position': this_group['position'], 'players': None}
                    players = []
                    for this_player in this_group['items']:
                        new_player = player.Player(this_player['id'], {
                            'league': self.league,
                            'sport': self.sport,
                            'baseUrl': 'https://site.web.api.espn.com/apis/common/v3/sports/{}/{}/athletes'.format(
                                self.sport, self.league)
                        })
                        players.append(new_player)
                    dictionary['players'] = players
                    rost.append(dictionary)
                self.roster = rost
            return self.roster
        except Exception as e:
            print(e)
