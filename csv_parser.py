import csv

limit = 3
limit_i = 0

content = []

with open('train.csv') as f:
    file_content = csv.reader(f, delimiter=';')
    ignore_header = True
    for row in file_content:
        if ignore_header:
            ignore_header = False
            continue
        
        print('Was:', row, sep = '\n')
        
        parsed = [
                  int(row[0]),  # purpose
                  row[1],       # date
                  row[2],       # region type
                  row[3],       # region
                  row[4],       # city
                  row[5],       # hex
                  float(row[6]),# lat ^v
                  float(row[7]),# lon <>
                  
                  *[(float(row[i]) if row[i] else 0.) for i in range(8, 8+30)],
                 ]
        
        print('Became:', parsed, sep = '\n')
        if limit_i == limit: break
        limit_i += 1
