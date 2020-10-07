import request
from typing import List, Union


def fix_sport_name(sport_name: str):
    if sport_name.lower() in ['mixed martial arts']:
        return 'mma'
    if sport_name.lower() in ['futbol']:
        return 'soccer'
    return sport_name.lower()


def fix_league_name(league_name: str):
    if league_name.lower() in ['college football', 'ncaaf', 'cfb']:
        return 'college-football'
    if league_name.lower() in ['ncaam', 'mcb', 'ncb', 'mens college basketball']:
        return 'mens-college-basketball'
    if league_name.lower() in ['ncaaw', 'wcb', 'ncw', 'womens college basketball']:
        return 'womens-college-basketball'
    return league_name.lower()


def get_team_id_from_name(team_object, keyword):
    json_data = request.get_json(f'{team_object.baseUrl}/teams/{keyword.lower()}')
    return json_data['teamInfo']['team']['id']


def get_nested_dict_value(dictionary: dict, ordered_list_of_keys: List, default_value=None):
    if nested_key_exist(dictionary=dictionary, ordered_list_of_keys=ordered_list_of_keys):
        point = dictionary
        for key in ordered_list_of_keys:
            point = point[key]
        return point
    return default_value


def nested_key_exist(dictionary: dict, ordered_list_of_keys: List) -> bool:
    point = dictionary
    for key in ordered_list_of_keys:
        if type(key) == int and type(point) == list:
            if -1 <= key < len(point):
                point = point[key]
        elif point.get(key):
            point = point[key]
        else:
            return False
    return True
