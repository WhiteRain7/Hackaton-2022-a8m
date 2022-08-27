from api import population
from api import wot

FILENAME = 'updated_wot.json'


def load_parced_data():
    population_data = population.get_data()
    wot_data = wot.get_data()

    print(population_data, wot_data)
