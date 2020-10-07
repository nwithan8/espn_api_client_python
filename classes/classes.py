import json
from typing import Union, List

import helpers
from request import get_json


class Player:
    def __init__(self, player_id: str, data: json):
        self.playerID = player_id
        self._data = data
        self.league = data.get('league')
        self.sport = data.get('sport')
        self.baseUrl = data.get('base_url')
        self.firstName = None
        self.lastName = None
        self.position = None
        self.jerseyNumber = None
        self._team = None
        self.update_player_info()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.sport}:{self.firstName}{self.lastName}>"

    def get_json(self) -> Union[dict, None]:
        try:
            return get_json(f'{self.baseUrl}/{self.playerID}')
        except Exception as e:
            print(e)
        return None

    def update_player_info(self) -> bool:
        try:
            json_data = self.get_json()
            if not json_data:
                return False
            if json_data.get('athlete'):
                json_data = json_data['athlete']
            try:
                self.firstName = json_data.get('firstName')
                self.lastName = json_data.get('lastName')
                self.jerseyNumber = json_data.get('jersey')
                self.position = helpers.get_nested_dict_value(dictionary=json_data,
                                                              ordered_list_of_keys=['position', 'abbreviation'])
                return True
            except Exception as e:
                print(f'Error in inner try: {e}')
        except Exception as e:
            print(f'Error in outer try: {e}')
        return False

    @property
    def team(self):
        if not self._team:
            json_data = self.get_json()
            if json_data and helpers.nested_key_exist(dictionary=json_data, ordered_list_of_keys=['athlete', 'team']):
                self._team = Team(team_id=helpers.get_nested_dict_value(dictionary=json_data,
                                                                        ordered_list_of_keys=['athlete', 'team', 'id']),
                                  data={
                                      'teamNickname': None,
                                      'league': self.league,
                                      'sport': self.sport,
                                      'base_url': f'http://site.api.espn.com/apis/site/v2/sports/{self.sport}/{self.league}'
                                  })
        return self._team

    @property
    def stats_summary(self) -> Union[dict, None]:
        json_data = self.get_json()
        return helpers.get_nested_dict_value(dictionary=json_data, ordered_list_of_keys=['athlete', 'statsSummary'])

    @property
    def full_stats(self) -> Union[dict, None]:
        if self.league:
            return get_json(f'{self.baseUrl}/{self.playerID}/splits')
        json_data = get_json(f'{self.baseUrl}/{self.playerID}/statisticslog')
        return json_data.get('entries')


class Game:
    def __init__(self, game_id: str, data: json):
        self.gameID = game_id
        self._data = data
        self.league = data.get('league')
        self.sport = data.get('sport')
        self.baseUrl = data.get('base_url')
        self._awayTeam = None
        self._homeTeam = None
        self.winProbability = {}
        self.spread = None
        self.overUnder = None
        self.venue = None
        self.attendance = None
        self.broadcast = None
        self._make_game()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.sport}:Game{self.gameID}>"

    def get_json(self) -> Union[dict, None]:
        try:
            return get_json(f'{self.baseUrl}/summary?event={self.gameID}')
        except Exception as e:
            print(e)
        return None

    def _make_game(self):
        try:
            json_data = self.get_json()
            if json_data:
                self.venue = {
                    'name': helpers.get_nested_dict_value(dictionary=json_data,
                                                          ordered_list_of_keys=['gameInfo', 'venue', 'fullName']),
                    'city': helpers.get_nested_dict_value(dictionary=json_data,
                                                          ordered_list_of_keys=['gameInfo', 'venue', 'address',
                                                                                'city']),
                    'state': helpers.get_nested_dict_value(dictionary=json_data,
                                                           ordered_list_of_keys=['gameInfo', 'venue', 'address',
                                                                                 'state']),
                    'capacity': helpers.get_nested_dict_value(dictionary=json_data,
                                                              ordered_list_of_keys=['gameInfo', 'venue', 'capacity']),
                    'image': (
                        helpers.get_nested_dict_value(dictionary=json_data,
                                                      ordered_list_of_keys=['gameInfo', 'venue', 'images', 0, 'href'])
                    )
                }
                self.attendance = (
                    helpers.get_nested_dict_value(dictionary=json_data,
                                                  ordered_list_of_keys=['gameInfo', 'venue', 'attendance'])
                )
                self.broadcast = (helpers.get_nested_dict_value(dictionary=json_data,
                                                                ordered_list_of_keys=['header', 'competitions', 0,
                                                                                      'broadcasts', 0, 'media',
                                                                                      'shortName']))
        except Exception as e:
            print(e)

    @property
    def teams(self) -> dict:
        if not self._homeTeam and not self._awayTeam:
            json_data = self.get_json()
            teams = helpers.get_nested_dict_value(dictionary=json_data, ordered_list_of_keys=['boxscore', 'teams'])
            if teams:
                self._awayTeam = Team(
                    team_id=helpers.get_nested_dict_value(dictionary=teams, ordered_list_of_keys=[0, 'team', 'id']),
                    data={
                        'league': self.league,
                        'sport': self.sport,
                        'base_url': self.baseUrl,
                        'teamNickname': None
                    })
                self._homeTeam = Team(
                    team_id=helpers.get_nested_dict_value(dictionary=teams, ordered_list_of_keys=[1, 'team', 'id']),
                    data={
                        'league': self.league,
                        'sport': self.sport,
                        'base_url': self.baseUrl,
                        'teamNickname': None
                    })
        return {'awayTeam': self._awayTeam, 'homeTeam': self._homeTeam}

    @property
    def homeTeam(self):
        if not self._homeTeam:
            _ = self.teams
        return self._homeTeam

    @property
    def awayTeam(self):
        if not self._awayTeam:
            _ = self.teams
        return self._awayTeam

    @property
    def score(self) -> dict:
        try:
            json_data = self.get_json()
            if json_data.get('scoringPlays'):
                last_score = helpers.get_nested_dict_value(dictionary=json_data,
                                                           ordered_list_of_keys=['scoringPlays', -1])
                if last_score:
                    return {'awayScore': last_score.get('awayScore', 0), 'homeScore': last_score.get('homeScore', 0)}
        except Exception as e:
            print(e)
        return {'awayScore': 0, 'homeScore': 0}

    @property
    def probability(self) -> dict:
        try:
            json_data = self.get_json()
            if json_data.get('winprobability'):
                last_probability = helpers.get_nested_dict_value(dictionary=json_data,
                                                                 ordered_list_of_keys=['winprobability', -1])
                if last_probability and last_probability.get('homeWinPercentage'):
                    if last_probability['homeWinPercentage'] < 0.5:
                        percentage = (1 - int(last_probability['homeWinPercentage'])) * 100
                        winning_team = self.awayTeam
                    else:
                        percentage = int(last_probability['homeWinPercentage']) * 100
                        winning_team = self.homeTeam
                    return {
                        'winningTeam': winning_team,
                        'percentage': percentage,
                    }
        except Exception as e:
            print(e)
        return {}

    @property
    def odds(self) -> dict:
        try:
            if not self.spread or not self.overUnder:
                json_data = self.get_json()
                if json_data.get('pickcenter'):
                    self.spread = helpers.get_nested_dict_value(dictionary=json_data,
                                                                ordered_list_of_keys=['pickcenter', 0, 'details'])
                    self.overUnder = helpers.get_nested_dict_value(dictionary=json_data,
                                                                   ordered_list_of_keys=['pickcenter', 0, 'overUnder'])
            return {
                'spread': self.spread,
                'overUnder': self.overUnder
            }
        except Exception as e:
            print(e)
        return {}


class Team:
    def __init__(self, team_id: str, data: dict):
        self.teamID = team_id
        self._data = data
        self.league = data.get('league')
        self.sport = data.get('sport')
        self.baseUrl = data.get('base_url')
        self.nickname = data.get('teamNickname')
        self.abbreviation = None
        self.location = None
        self.mascot = None
        self.displayName = None
        self.color = None
        self.teamLogoURL = None
        self._conference = None
        self.links = {}
        self._schedule = []
        self.statistics = {}
        self.record = {}
        self._roster = []
        self._make_team()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.sport}:{self.displayName}>"

    def get_json(self) -> Union[dict, None]:
        try:
            return get_json(f'{self.baseUrl}/teams/{self.teamID}')
        except Exception as e:
            print(e)
        return None

    def _make_team(self):
        try:
            json_data = self.get_json()
            if json_data.get('team'):
                self.nickname = helpers.get_nested_dict_value(dictionary=json_data,
                                                              ordered_list_of_keys=['team', 'nickname'])
                self.abbreviation = helpers.get_nested_dict_value(dictionary=json_data,
                                                                  ordered_list_of_keys=['team', 'abbreviation'])
                self.location = helpers.get_nested_dict_value(dictionary=json_data,
                                                              ordered_list_of_keys=['team', 'location'])
                self.mascot = helpers.get_nested_dict_value(dictionary=json_data, ordered_list_of_keys=['team', 'name'])
                self.displayName = helpers.get_nested_dict_value(dictionary=json_data,
                                                                 ordered_list_of_keys=['team', 'displayName'])
                self.color = helpers.get_nested_dict_value(dictionary=json_data, ordered_list_of_keys=['team', 'color'])
                self.teamLogoURL = helpers.get_nested_dict_value(dictionary=json_data,
                                                                 ordered_list_of_keys=['team', 'logos', 0, 'href'])
                self.record = {
                    'wins': helpers.get_nested_dict_value(dictionary=json_data,
                                                          ordered_list_of_keys=['team', 'record', 'items', 0, 'stats',
                                                                                1, 'value']),
                    'losses': helpers.get_nested_dict_value(dictionary=json_data,
                                                            ordered_list_of_keys=['team', 'record', 'items', 0, 'stats',
                                                                                  2, 'value']),
                    'ties': helpers.get_nested_dict_value(dictionary=json_data,
                                                          ordered_list_of_keys=['team', 'record', 'items', 0, 'stats',
                                                                                5, 'value'])
                }
                self.statistics = helpers.get_nested_dict_value(dictionary=json_data,
                                                                ordered_list_of_keys=['team', 'record', 'items']),
                self.links = helpers.get_nested_dict_value(dictionary=json_data, ordered_list_of_keys=['team', 'links'])
        except Exception as e:
            print(e)

    @property
    def schedule(self) -> List[Game]:
        try:
            if not self._schedule:
                json_data = get_json(f'{self.baseUrl}/teams/{self.teamID}/schedule')
                schedule = []
                if json_data.get('events'):
                    for game in json_data['events']:
                        new_game = Game(game_id=game.get('id'),
                                        data={
                                            'league': self.league,
                                            'sport': self.sport,
                                            'base_url': self.baseUrl
                                        })
                        schedule.append(new_game)
                    self._schedule = schedule
            return self._schedule
        except Exception as e:
            print(e)
        return []

    @property
    def conference(self):
        try:
            if not self._conference:
                json_data = self.get_json()
                self._conference = Conference(conference_id=helpers.get_nested_dict_value(dictionary=json_data,
                                                                                          ordered_list_of_keys=['team',
                                                                                                                'groups',
                                                                                                                'id']),
                                              data={
                                                  'league': self.league,
                                                  'sport': self.sport,
                                                  'base_url': self.baseUrl
                                              })
            return self._conference
        except Exception as e:
            print(e)
        return None

    @property
    def roster(self) -> dict:
        try:
            if not self._roster:
                json_data = get_json(f'{self.baseUrl}/teams/{self.teamID}/roster')
                roster = []
                for group in json_data.get('athletes', []):
                    dictionary = {
                        'position': group.get('position'),
                        'players': None
                    }
                    players = []
                    for this_player in group.get('items', []):
                        new_player = Player(this_player.get('id'), {
                            'league': self.league,
                            'sport': self.sport,
                            'base_url': f'https://site.web.api.espn.com/apis/common/v3/sports/{self.sport}/{self.league}/athletes'
                        })
                        players.append(new_player)
                    dictionary['players'] = players
                    roster.append(dictionary)
                self._roster = roster
            return self._roster
        except Exception as e:
            print(e)
        return {}


class Conference:
    def __init__(self, conference_id: str, data: dict):
        self.conferenceID = conference_id
        self._data = data
        self.league = data['league']
        self.sport = data['sport']
        self.baseUrl = data['base_url']
        self.name = None
        self._teams = []

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.sport}:Conference{self.conferenceID}>"

    @property
    def teams(self) -> List[Team]:
        try:
            if not self._teams:
                self._teams = []
                json_data = get_json(f'{self.baseUrl}/teams?groups={self.conferenceID}&limit=1000')
                for team in helpers.get_nested_dict_value(dictionary=json_data,
                                                          ordered_list_of_keys=['sports', 0, 'leagues', 0, 'teams'],
                                                          default_value=[]):
                    new_team = Team(
                        team_id=helpers.get_nested_dict_value(dictionary=team, ordered_list_of_keys=['team', 'id']),
                        data={
                            'league': self.league,
                            'sport': self.sport,
                            'base_url': self.baseUrl,
                            'teamNickname': None
                        })
                    self._teams.append(new_team)
            return self._teams
        except Exception as e:
            print(e)
        return []


class League:
    def __init__(self, league_name: str, data: json):
        self.league = league_name
        self._data = data
        self.sport = data.get('sport')
        self.baseUrl = data.get('base_url')
        self._teams = []
        self._conferences = []
        self._rankings = {}
        self._currentGames = []

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.sport}:{self.league}>"

    @property
    def teams(self) -> List[Team]:
        try:
            if not self._teams:
                json_data = get_json(f'{self.baseUrl}/teams?limit=1000')
                for team in helpers.get_nested_dict_value(dictionary=json_data,
                                                          ordered_list_of_keys=['sports', 0, 'leagues', 0, 'teams'],
                                                          default_value=[]):
                    self._teams.append(
                        Team(
                            team_id=helpers.get_nested_dict_value(dictionary=team, ordered_list_of_keys=['team', 'id']),
                            data={
                                'league': self.league,
                                'sport': self.sport,
                                'base_url': self.baseUrl,
                                'teamNickname': None
                            })
                    )
            return self._teams
        except Exception as e:
            print(e)
        return []

    def team(self, team_id: str) -> Union[Team, None]:
        try:
            if not team_id.isnumeric():
                team_id = helpers.get_team_id_from_name(team_object=self, keyword=team_id.lower())
            if team_id:
                return Team(team_id=team_id,
                            data={
                                'teamNickname': None,
                                'league': self.league,
                                'sport': self.sport,
                                'base_url': self.baseUrl
                            })
        except Exception as e:
            print(e)
        return None

    # TODO Endpoint for this?
    @property
    def conferences(self) -> List[Conference]:
        return []

    def conference(self, conference_id: str) -> Union[Conference, None]:
        try:
            return Conference(conference_id=conference_id,
                              data={
                                  'league': self.league,
                                  'sport': self.sport,
                                  'base_url': self.baseUrl
                              })
        except Exception as e:
            print(e)
        return None

    def game(self, game_id: str) -> Union[Game, None]:
        try:
            return Game(game_id=game_id,
                        data={
                            'league': self.league,
                            'sport': self.sport,
                            'base_url': self.baseUrl
                        })
        except Exception as e:
            print(e)
        return None

    def player(self, player_id: str) -> Union[Player, None]:
        try:
            return Player(player_id=player_id,
                          data={
                              'league': self.league,
                              'sport': self.sport,
                              'base_url': f'https://site.web.api.espn.com/apis/common/v3/sports/{self.sport}/{self.league}/athletes'
                          })
        except Exception as e:
            print(e)
        return None

    @property
    def rankings(self) -> dict:
        try:
            json_data = get_json(f'{self.baseUrl}/rankings')
            self._rankings = json_data
            return self._rankings
        except Exception as e:
            print(e)
        return {}

    @property
    def news(self) -> dict:
        try:
            json_data = get_json(f'{self.baseUrl}/news')
            return json_data
        except Exception as e:
            print(e)
        return {}

    @property
    def current_games(self) -> List[Game]:
        try:
            self._currentGames = []
            json_data = get_json(f'{self.baseUrl}/scoreboard')
            for game in helpers.get_nested_dict_value(dictionary=json_data, ordered_list_of_keys=['events'],
                                                      default_value=[]):
                new_game = Game(game_id=game.get('id'),
                                data={
                                    'league': self.league,
                                    'sport': self.sport,
                                    'base_url': self.baseUrl
                                })
                self._currentGames.append(new_game)
            return self._currentGames
        except Exception as e:
            print(e)
        return []


class Sport:
    def __init__(self, sport_name: str, data: json):
        self.sport = sport_name
        self.baseUrl = data.get('base_url')

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.sport}>"

    def league(self, league_name: str) -> Union[League, None]:
        try:
            proper_league = helpers.fix_league_name(league_name=league_name)
            return League(league_name=proper_league,
                          data={
                              'sport': self.sport,
                              'base_url': f'{self.baseUrl}/{proper_league}'
                          })
        except Exception as e:
            print(e)
        return None

    def player(self, player_id: str) -> Union[Player, None]:
        try:
            return Player(player_id=player_id,
                          data={
                              'league': None,
                              'sport': self.sport,
                              'base_url': f'http://sports.core.api.espn.com/v2/sports/{self.sport}/athletes'
                          })
        except Exception as e:
            print(e)
        return None
