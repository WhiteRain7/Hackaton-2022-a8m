import csv
import datetime
from user_by_city import load_parced_data, get_percent_by_city

def parse(filename = 'train.csv', limit = 10000, step = 1, print_logs = True):
    data = load_parced_data()
    limit_i = 0
    if limit:
        if limit < 0: limit = 1
        limit -= 1
        limit_ten_percents = limit // 10
        if limit_ten_percents == 0: limit_ten_percents = 1
    
    content = {'X': [], 'Y': []}
    
    with open(filename, encoding = 'utf-8') as f:
        if print_logs: print('Parsing file "{}".'.format(filename))
        
        file_content = csv.reader(f, delimiter=';')
        
        for i, row in enumerate(file_content):
            if i%step != 0 or i == 0: continue
                    
            parsedX = [
                float(get_percent_by_city(row[4], data)),
                float(row[6])/180, # ^v
                float(row[7])/180, # <>
                int(datetime.datetime.fromisoformat(row[1]).timestamp())/10e9,
                *[(float(row[i]) if row[i] else 0.) for i in range(8, 8+30)] # f1-f30
            ]
            
            parsedY = [int(row[0])] # purpose

            content['X'].append(parsedX)
            content['Y'].append(parsedY)

            if limit:
                if limit_i % limit_ten_percents == 0:
                    if print_logs: print('Still parsing... {}0%'.format(limit_i // limit_ten_percents))
                if limit_i >= limit: break
                limit_i += 1
            elif print_logs and i%30000 == 0: print('Still parsing... iter #{}'.format(i))

    if print_logs: print('Parsing finished.\n')
    return content
