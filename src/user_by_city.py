import pathlib

from api import population
from api import wot
from utils import to_float, read_file_to_list, write_list_to_file

FILENAME = 'updated_wot.json'


def get_percent_by_city(city: str, data: dict) -> float:
    users = data.get(city)
    if not users:
        return 0
    return to_float(users)


def load_parced_data() -> dict:
    if (not pathlib.Path(FILENAME).is_file()):
        population_data = population.get_data()
        wot_data = wot.get_data()

        all_players = wot.get_all_users(wot_data)
        middle_percent_players_in_city = all_players / population.RUSSIA_POPULATION
        min_percent_players = 0
        max_percent_players = 0
        for item in wot_data:
            population_in_city = population.get_population_by_city(
                item['city'], population_data)
            percent_players_in_city = to_float(
                item.get('users')) / population_in_city
            if (percent_players_in_city > max_percent_players):
                max_percent_players = percent_players_in_city

        flag = False
        data = {}
        for i, item in enumerate(wot_data):
            population_in_city = population.get_population_by_city(
                item['city'], population_data)
            percent_players_in_city = to_float(
                item.get('users')) / population_in_city
            if (percent_players_in_city < middle_percent_players_in_city):
                percent_players_in_city = (
                    percent_players_in_city -
                    min_percent_players) / middle_percent_players_in_city * .5
            else:
                percent_players_in_city = (
                    percent_players_in_city - middle_percent_players_in_city
                ) / (max_percent_players -
                     middle_percent_players_in_city) * .5 + .5
            data.update({item['city']:percent_players_in_city})
        write_list_to_file(FILENAME, data)
    else:
        data = read_file_to_list(FILENAME)
    return data
