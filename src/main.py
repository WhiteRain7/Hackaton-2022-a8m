import time
import pathlib

import csv_parser
import predict
from user_by_city import load_parced_data


def get_time(func):
    def wrap (*args, **kwargs):
        time_at_start = time.perf_counter()
        result = func(*args, **kwargs)
        print('Func takes {} seconds\n'.format(time.perf_counter() - time_at_start))
        return result
    return wrap

def main(): # 152 767 ## 14 000 awans
    data = load_parced_data()
    filename = pathlib.Path(__file__).parent.parent.absolute() / 'train.csv'
    parsed_data = get_time(csv_parser.parse)(filename, limit = 14000, step = 1)
    y_pred, model = get_time(predict.nn_learning)(parsed_data, iterations = 500, learning_rate = 1e-5)

    check_data = get_time(csv_parser.parse)('test.csv', limit = 14000, step = 1)
    result = predict.predict_all(check_data['X'], model)
    
    print('===============================================================\n')

    print('----------------------------------------------------------')
    print('Start verifying learning...')
    print('----------------------------------------------------------')
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

    print()
    print('----------------------------------------------------------')
    print('Start verifying prediction...')
    print('----------------------------------------------------------\n')
    ys = result.tolist()
    for i in range(len(ys)): ys[i].append(i) # [[buy-ratio, user_num], ...]
    ys.sort(reverse = True)
    
    best_nums = 15
    print('Best {} positions:'.format(best_nums))
    for i in range(best_nums):
        verified = (check_data['Y'][ys[i][1]][0] == max(min(round(ys[i][0]), 1), 0))
        print('{:>3}) #{:<7} ({:>5}) - {}'.format(i+1, ys[i][1], round(ys[i][0], 2), verified))

    print()
    worst_nums = 15
    print('Worst {} positions:'.format(worst_nums))
    for i in range(-1, -worst_nums-1, -1):
        verified = (check_data['Y'][ys[i][1]][0] == max(min(round(ys[i][0]), 1), 0))
        print('{:>3}) #{:<7} ({:>5}) - {}'.format(i, ys[i][1], round(ys[i][0], 2), verified))

    verify_percents = .05
    top_percent_content = []
    zeros = 0
    verified_zeros = 0
    awans = 0
    verified_awans = 0
    
    for i in range(int(len(ys)*verify_percents)):
        top_percent_content.append(ys[i])
        ratio = max(min(round(ys[i][0]), 1), 0)
        verified = (check_data['Y'][ys[i][1]][0] == ratio)
            
        if ratio == 1: awans += 1
        else: zeros += 1
        if verified:
            if ratio == 1: verified_awans += 1
            else: verified_zeros += 1

    print()
    print('From {} output values picked {}%, so here\'s a top {}:'.format(len(ys), verify_percents*100, int(len(ys)*verify_percents)))
    print(' - zeros:', zeros)
    if zeros != 0: print(' - verified zeros:', verified_zeros / zeros)
    print()
    print(' - awans:', awans)
    if awans != 0: print(' - verified awans:', verified_awans / awans)

    return top_percent_content

main()
