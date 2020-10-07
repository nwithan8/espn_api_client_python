from typing import Union, List

from classes.classes import Sport
import helpers


class ESPN:

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def sport(self, sport_name: str) -> Union[Sport, None]:
        try:
            proper_sport = helpers.fix_sport_name(sport_name=sport_name)
            return Sport(sport_name=proper_sport, data={
                'base_url': f'https://site.api.espn.com/apis/site/v2/sports/{proper_sport}'
            })
        except Exception as e:
            print(e)
        return None
