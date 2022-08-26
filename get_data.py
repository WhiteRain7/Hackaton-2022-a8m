import requests

URL = 'https://web.archive.org/web/20190514155638if_/http://www.wotext.ru/map/getcities'


def get_item_by_city(data, city):
    return list(filter(lambda i, city=city: i['city'] == city, data))


def get_data():
    parsed_date = requests.get(URL)
    parsed_date = parsed_date.json()
    data = filter(lambda i: i['country'] == 'RU', parsed_date)
    return data


def main():
    data = get_data()
    print(get_item_by_city(data, 'Москва'))


if __name__ == '__main__':
    main()
