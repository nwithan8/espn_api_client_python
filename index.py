import sport


class ESPN:

    def Sport(self, sportName):
        try:
            properSport = self.fixSportName(sportName)
            this_sport = sport.Sport(properSport, {
                'baseUrl': 'https://site.api.espn.com/apis/site/v2/sports/{}'.format(properSport)
            })
            return this_sport
        except Exception as e:
            print(e)

    def fixSportName(self, sport):
        if sport.lower() in ['mixed martial arts']:
            return 'mma'
        if sport.lower() in ['futbol']:
            return 'soccer'
        return sport.lower()
