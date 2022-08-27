from pathlib import Path

from utils import (to_float, read_file_to_list, write_list_to_file,
                   get_json_from_url)

URL = 'https://web.archive.org/web/20190514155638if_/http://www.wotext.ru/map/getcities'
FILE_API_SAVE = 'wot_api.json'


def get_all_users(data):
    all_users = 0
    for item in data:
        users = get_users_by_city(item['city'], data)
        all_users += users
    return all_users


def get_users_by_city(city: str, data: list) -> float:
    item = list(filter(lambda i, city=city: i['city'] == city, data))
    if len(item) == 0:
        return 0
    return to_float(item[0].get('users'))


def get_data(url: str = URL) -> list:
    path = Path(FILE_API_SAVE)
    if not path.is_file():
        try:
            parsed_data = get_json_from_url(url)
            ru_data = list(filter(lambda i: i['country'] == 'RU', parsed_data))
            write_list_to_file(FILE_API_SAVE, ru_data)
            return ru_data
        except Exception as e:
            print(e)
            return []
    else:
        ru_data = read_file_to_list(FILE_API_SAVE)
        return ru_data


def main():
    data = get_data()
    print(get_users_by_city('Москва', data))


if __name__ == '__main__':
    main()
