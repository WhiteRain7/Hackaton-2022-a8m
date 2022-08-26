import csv

limit = 5
limit_i = 0

content = []

with open('test.csv') as f:
    file_content = csv.reader(f, delimiter=';')
    for row in file_content:
        print(row)
        if limit_i == limit: break
        limit_i += 1
