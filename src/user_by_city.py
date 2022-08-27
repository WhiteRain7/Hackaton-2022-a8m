import pathlib

from api import population
from api import wot
from utils import to_float, read_file_to_list, write_list_to_file

FILENAME = 'updated_wot.json'


def get_percent_by_city(city: str, data: list) -> float:
    item = list(filter(lambda i, city=city: i['city'] == city, data))
    if len(item) == 0:
        return 0
    return to_float(item[0].get('percent_of_users'))


def load_parced_data() -> list:
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
        for i, item in enumerate(wot_data):
            population_in_city = population.get_population_by_city(
                item['city'], population_data)
            percent_players_in_city = to_float(
                item.get('users')) / population_in_city
            if (percent_players_in_city < middle_percent_players_in_city):
                item['percent_of_users'] = (
                    percent_players_in_city -
                    min_percent_players) / middle_percent_players_in_city * .5
            else:
                item['percent_of_users'] = (
                    percent_players_in_city - middle_percent_players_in_city
                ) / (max_percent_players -
                     middle_percent_players_in_city) * .5 + .5
            wot_data[i] = item
        write_list_to_file(FILENAME, wot_data)
    else:
        wot_data = read_file_to_list(FILENAME)
    return wot_data
