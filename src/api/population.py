import requests
import lxml.html
from pathlib import Path

from utils import (to_float, read_file_to_list, write_list_to_file)

URL = 'https://rusmap.net/Население_России'
FILE_API_SAVE = 'population_api.json'
RUSSIA_POPULATION = 145478097


def fix_parced_data(data: list) -> list:
    fixed_data = {
        'Киров': 500000.0,
        'Благовещенск': 224962.0,
    }
    add = {
        'Зеленоград': 253687.0,
    }
    for i, item in enumerate(data):
        item[0] = item[0].replace('ё', 'е')
        if (item[0] in fixed_data.keys()):
            data[i] = [item[0], fixed_data.get(item[0])]
    for x, v in add.items():
        data.append([x, v])
    # print(data)
    return data


def get_population_by_city(city: str, data: list) -> float:
    population = list(filter(lambda i, city=city: i[0] == city, data))
    if len(population) > 0 and population[0][1] > 10000:
        population = to_float(population[0][1])
    else:
        population = 100000.0
    return population


def get_data(url: str = URL) -> list:
    path = Path(FILE_API_SAVE)
    if not path.is_file():
        try:
            page = requests.get(url)
            html = lxml.html.fromstring(page.content)
            table = html.xpath(".//table//tbody")[0]
            data = []
            for tr in table.xpath("tr"):
                city = tr.xpath('th')[0].text_content()
                population = tr.xpath('td')[-1].text_content().replace(' ', '')
                data.append([city, to_float(population)])
            data = fix_parced_data(data)
            write_list_to_file(FILE_API_SAVE, data)
            return data
        except Exception as e:
            print(e)
            return []
    else:
        data = read_file_to_list(FILE_API_SAVE)
        return data


def main():
    data = get_data()
    s = sum([to_float(x[1]) for x in data])
    print(s)

    print(get_population_by_city('Санкт-Петербург', data))


if __name__ == '__main__':
    main()
