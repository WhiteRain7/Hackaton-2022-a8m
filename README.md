# Hackaton - 2022 - A&M

### [A8M.csv лежит в src/files](https://github.com/WhiteRain7/Hackaton-2022-a8m/blob/main/src/files/A8M.csv)
### Как запустить проект

- Внутри папки **src** создать папку **files**
- Переместить туда **train.csv** (для обучения) и **test.csv** (для предсказывания)
- Запустить **main.py**

### Требования

- python 3.10.5
- установить зависимости из requirements.txt
  - pytorch
  - requests
  - lxml
  
### Структура проекта

- **main.py** - главный файл
- **csv_parser.py** - получение входных и выходных значений, преобразование данных
- **predict.py** - функции создания и обучения нейросети, предсказание по имеющейся нейросети
- **user_by_city.py** - получение статистики по игрокам World of Tanks (WoT) для csv_parser.py
- **api**
  - **wot.py** - api к фанатскому сайту WoT, получение статистики по городам
  - **population.py** - парсинг сайта с численностью населения городов России
- **utils.py** - дополнительные функции для api и user_by_city.py

### Участники проекта

- [Макаров Максим](https://github.com/WhiteRain7), 1248857 - машинное обучение, тимлид
- [Малахов Максим](https://github.com/mrgick), 412185990 - обогащение данных
- [Никифоров Глеб](https://github.com/GlebNikiforov), 1206672 - анализ данных
