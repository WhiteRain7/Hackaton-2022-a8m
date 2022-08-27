import csv_parser
import api.wot as wot
import predict

import time

def get_time(func):
    def wrap (*args, **kwargs):
        time_at_start = time.perf_counter()
        result = func(*args, **kwargs)
        print('Func takes {} seconds\n'.format(time.perf_counter() - time_at_start))
        return result
    return wrap

def main(): # 152 767 ## 14 000 awans
    parsed_data = get_time(csv_parser.parse)(limit = 14000, step = 1)
    y_pred = get_time(predict.predict)(parsed_data, iterations = 1000)

    print('Start verifying')
    y_pred = y_pred.t().tolist()[0]

    all_ = len(parsed_data['Y'])
    verified = 0

    zeros = 0
    verified_zeros = 0
    awans = 0
    verified_awans = 0

    for i in range(len(parsed_data['Y'])):
        item_pred = round(y_pred[i], 2)
        item      = parsed_data['Y'][i][0]
        items_equals = (round(item_pred) == item)

        if items_equals: verified += 1

        if item == 0:
            zeros += 1
            if items_equals: verified_zeros += 1

        if item == 1:
            awans += 1
            if items_equals: verified_awans += 1

        if len(parsed_data['Y']) < 100:
            print('{:>13}'.format('{} - {} - {}'.format(item_pred, item, 'T' if items_equals else 'F')), end = '  ')
            if i%5 == 4: print()

    print()
    print('All:', all_)
    print('Verified successfully: {}%'.format(round(verified / all_ * 100, 2)))
    print()
    print('Zeros:', zeros)
    if zeros > 0: print('Verified zeros: {}%'.format(round(verified_zeros / zeros * 100, 2)))
    print()
    print('Awans:', awans)
    if awans > 0: print('Verified awans: {}%'.format(round(verified_awans / awans * 100, 2)))
    
main()
