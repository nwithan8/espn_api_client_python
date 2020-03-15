import league
import player


def fixLeagueName(league):
    if league.lower() in ['college football', 'ncaaf', 'cfb']:
        return 'college-football'
    if league.lower() in ['ncaam', 'mcb', 'ncb', 'mens college basketball']:
        return 'mens-college-basketball'
    if league.lower() in ['ncaaw', 'wcb', 'ncw', 'womens college basketball']:
        return 'womens-college-basketball'
    return league.lower()


class Sport:
    def __init__(self, sportName, data):
        self.sport = sportName
        self.baseUrl = data['baseUrl']

    def League(self, leagueName):
        try:
            properLeague = fixLeagueName(leagueName)
            l = league.League(properLeague, {
                'sport': self.sport,
                'baseUrl': '{}/{}'.format(self.baseUrl, properLeague)
            })
            return l
        except Exception as e:
            print(e)

    def Player(self, playerID):
        return player.Player(playerID, {
            'league': None,
            'sport': self.sport,
            'baseUrl': 'http://sports.core.api.espn.com/v2/sports/{}/athletes'.format(self.sport)
        })
