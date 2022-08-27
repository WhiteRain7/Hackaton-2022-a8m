from .utils import (to_float, read_file_to_list, write_list_to_file,
                    get_json_from_url)
from pathlib import Path

URL = 'https://pomber.github.io/covid19/timeseries.json'
FILE_API_SAVE = 'corona_api.json'


def get_daily_confirmed_by_day(day: str, data) -> float:

    return 0


def get_data(url: str = URL) -> list:
    path = Path(FILE_API_SAVE)
    if not path.is_file():
        try:
            parsed_data = get_json_from_url(url)
            ru_data = parsed_data['Russia']
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
    print(get_item_by_city('Москва', data))


if __name__ == '__main__':
    main()
