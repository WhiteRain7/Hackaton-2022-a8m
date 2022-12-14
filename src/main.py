import time
import pathlib
import pickle

import csv_parser
import predict

DIRECTORY_FILES = pathlib.Path(__file__).parent.absolute() / 'files' 

def get_time(func):
    def wrap (*args, **kwargs):
        time_at_start = time.perf_counter()
        result = func(*args, **kwargs)
        print('Func takes {} seconds\n'.format(time.perf_counter() - time_at_start))
        return result
    return wrap

def main(get_nn_from = None, # path/to/binary/file or None to learn new nn
         save_as = None,     # ONLY IF GET__NN_FROM IS NONE: if save_as is str, save nn as binary file with at save_as path, else will not save
         print_logs = True,  # if True, python will print logs to console (else will not do any logs)
         ):

    if get_nn_from is None:
        filename = DIRECTORY_FILES / 'train.csv'  # 152 767 ## 14 000 ones
        parsed_data = get_time(csv_parser.parse)(filename, limit = 14000, step = 1, print_logs = print_logs)

        y_pred, model = get_time(predict.nn_learning)(parsed_data,
                                                      iterations = 100,
                                                      learning_rate = 1e-6,
                                                      min_accuracy = None,
                                                      forced_exit = False,
                                                      auto_reiterate = True,
                                                      max_renews = 2,
                                                      per_iter = 1,
                                                      print_logs = print_logs)

        if save_as is not None:
            with open(save_as, 'wb') as f: pickle.dump(model, f)

    else: # if get_nn_from is path, not None
        with open(get_nn_from, 'rb') as f: model = pickle.load(f)

    filename = DIRECTORY_FILES / 'test dataset.csv'
    check_data = get_time(csv_parser.parse)(filename, limit = 0, step = 1)
    result = predict.predict_all(check_data['X'], model)

    if print_logs:
        print('===============================================================\n')
        
        if get_nn_from is None:
            round_border = .5 # if less than round_border, answer is 0, else 1

            print('----------------------------------------------------------')
            print('Start verifying learning...')
            print('----------------------------------------------------------')
            y_pred = y_pred.t().tolist()[0]

            all_ = len(parsed_data['Y'])
            verified = 0

            zeros = 0
            verified_zeros = 0
            ones = 0
            verified_ones = 0

            for i in range(len(parsed_data['Y'])):
                item_pred    = round(y_pred[i], 2)
                item         = parsed_data['Y'][i][0]
                items_equals = ((0 if item_pred < round_border else 1) == item)

                if items_equals: verified += 1

                if item == 0:
                    zeros += 1
                    if items_equals: verified_zeros += 1

                if item == 1:
                    ones += 1
                    if items_equals: verified_ones += 1

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
            print('Ones:', ones)
            if ones > 0: print('Verified ones: {}%'.format(round(verified_ones / ones * 100, 2)))

        print()
        print('----------------------------------------------------------')
        print('Start verifying prediction...')
        print('----------------------------------------------------------\n')
        ys = result.tolist()
        for i in range(len(ys)): ys[i].append(i) # [[buy-ratio, user_num], ...]
        ys.sort(reverse = True)

        zeros = 0
        ones = 0
        for i in range(len(ys)):
            if check_data['Y'][ys[i][1]][0] == 0: zeros += 1
            else: ones += 1

        print()
        print('Here\'s in test file:')
        print('Zeros:', zeros)
        print('Ones:', ones)

        # if less than round_border, answer is 0, else 1
        round_border = ys[-1][0] + (ys[0][0] - ys[-1][0]) / (zeros / (1 if ones == 0 else ones) + 1)
        print('Round border:', round_border)
        print()

        best_nums = 15
        print('Best {} positions:'.format(best_nums))
        for i in range(best_nums):
            verified = (check_data['Y'][ys[i][1]][0] == (0 if ys[i][0] < round_border else 1))
            print('{:>3}) #{:<7} ({:>5}) - {}'.format(i+1, ys[i][1], round(ys[i][0], 2), verified))

        print()
        median_nums = 15
        print('Median {} positions:'.format(median_nums))
        for i in range(len(ys)//2 - median_nums//2, len(ys)//2 + median_nums//2 + 1):
            verified = (check_data['Y'][ys[i][1]][0] == (0 if ys[i][0] < round_border else 1))
            print('{:>3}) #{:<7} ({:>5}) - {}'.format(i+1, ys[i][1], round(ys[i][0], 2), verified))

        print()
        worst_nums = 15
        print('Worst {} positions:'.format(worst_nums))
        for i in range(-1, -worst_nums-1, -1):
            verified = (check_data['Y'][ys[i][1]][0] == (0 if ys[i][0] < round_border else 1))
            print('{:>3}) #{:<7} ({:>5}) - {}'.format(i, ys[i][1], round(ys[i][0], 2), verified))

        verify_percents = .05
        top_percent_content = []
        zeros = 0
        verified_zeros = 0
        ones = 0
        verified_ones = 0

        for i in range(int(len(ys)*verify_percents)):
            top_percent_content.append([ys[i][1], ys[i][0]])
            ratio = (0 if ys[i][0] < round_border else 1)
            verified = (check_data['Y'][ys[i][1]][0] == ratio)

            if ratio == 1: ones += 1
            else: zeros += 1
            if verified:
                if ratio == 1: verified_ones += 1
                else: verified_zeros += 1

        print()
        print('From {} output values picked {}%, so here\'s a top {}:'.format(len(ys), verify_percents*100, int(len(ys)*verify_percents)))
        print('Zeros:', zeros)
        if zeros > 0: print('Verified zeros: {}%'.format(round(verified_zeros / zeros * 100, 2)))
        print()
        print('Ones:', ones)
        if ones > 0: print('Verified ones: {}%'.format(round(verified_ones / ones * 100, 2)))

    return top_percent_content

def save_to_csv(data: list, filename: str = DIRECTORY_FILES / 'A8M.csv'):
    import csv
    with open(filename, 'w', newline='\n', encoding = 'utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(['id','label'])
        for item in data:
            spamwriter.writerow([item[0]+1,item[1]])

if __name__ == '__main__':
    model = DIRECTORY_FILES / 'model_3_99'
    if (model.is_file()):
        result = main(get_nn_from=model)
    else:
        result = main(save_as=model)
    save_to_csv(result)
