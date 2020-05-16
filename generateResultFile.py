import xlwings as xw
from dict import *

data_seq = [1, 2, 3, 4, 5]
cm_seq = [1, 2]
prod_seq = [1, 2]
wd_seq = [1, 2, 3]
model_seq = [
    [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 0],
    [2, 0, 1], [2, 1, 1], [2, 0, 0], [2, 1, 0],
    [3, 0, 1], [3, 1, 1], [3, 0, 0], [3, 1, 0],
    [4, 0, 1], [4, 1, 1], [4, 0, 0], [4, 1, 0],
    [5, 0, 1], [5, 1, 1], [5, 0, 0], [5, 1, 0],
    [6, 0, 0], [7, 0, 0], [8, 0, 1], [8, 0, 0], [9, 0, 1], [9, 0, 0]
]

for data_key in data_seq:
    data_name = dataset_name_dict[data_key]
    for cm_key in cm_seq:
        cm_name = cascade_model_dict[cm_key]
        profit_max_list, profit_mean_list, profit_min_list, time_max_list, time_mean_list, time_min_list = [], [], [], [], [], []
        for bi in range(10, 6, -1):
            for prod_key in prod_seq:
                prod_name = product_name_dict[prod_key]
                for wallet_key in wd_seq:
                    wallet_type = wallet_distribution_type_dict[wallet_key]

                    profit_max, profit_mean, profit_min, time_max, time_mean, time_min = [], [], [], [], [], []
                    profit_max_dict, profit_mean_dict, profit_min_dict = {model_name: '' for model_name in model_seq}, {model_name: '' for model_name in model_seq}, {model_name: '' for model_name in model_seq}
                    time_max_dict, time_mean_dict, time_min_dict = {model_name: '' for model_name in model_seq}, {model_name: '' for model_name in model_seq}, {model_name: '' for model_name in model_seq}
                    r = data_name + '\t' + cm_name + '\t' + wallet_type + '\t' + prod_name + '\t' + str(bi)
                    print(r)
                    for mn_list in model_seq:
                        model_name = get_model_name(mn_list)
                        for times in range(10):
                            try:
                                result_name = 'result/' + \
                                              data_name + '_' + cm_name + '/' + \
                                              wallet_type + '_' + prod_name + '_bi' + str(bi) + '/' + \
                                              model_name + '_' + str(times) + '.txt'

                                with open(result_name) as f:
                                    p = 0.0
                                    for lnum, line in enumerate(f):
                                        if lnum < 2 or lnum == 3:
                                            continue
                                        elif lnum == 2:
                                            (l) = line.split()
                                            t = float(l[-1])
                                            if times == 0:
                                                time_max_dict[model_name] = t
                                                time_mean_dict[model_name] = t
                                                time_min_dict[model_name] = t
                                            else:
                                                time_max_dict[model_name] = max(t, time_max_dict[model_name])
                                                time_mean_dict[model_name] = round((time_mean_dict[model_name] * times + t) / (times + 1), 4)
                                                time_min_dict[model_name] = min(t, time_max_dict[model_name])
                                        elif lnum == 4:
                                            (l) = line.split()
                                            p = float(l[-1])
                                        elif lnum == 5:
                                            (l) = line.split()
                                            c = float(l[-1])
                                            pro = round(p - c, 4)
                                            if times == 0:
                                                profit_max_dict[model_name] = pro
                                                profit_mean_dict[model_name] = pro
                                                profit_min_dict[model_name] = pro
                                            else:
                                                profit_max_dict[model_name] = max(pro, profit_max_dict[model_name])
                                                profit_mean_dict[model_name] = round((profit_mean_dict[model_name] * times + pro) / (times + 1), 4)
                                                profit_min_dict[model_name] = min(pro, profit_min_dict[model_name])
                                        else:
                                            break
                            except FileNotFoundError:
                                continue
                        profit_max.append(str(profit_max_dict[model_name]))
                        profit_mean.append(str(profit_mean_dict[model_name]))
                        profit_min.append(str(profit_min_dict[model_name]))
                        time_max.append(str(time_max_dict[model_name]))
                        time_mean.append(str(time_mean_dict[model_name]))
                        time_min.append(str(time_min_dict[model_name]))
                    profit_max_list.append(profit_max)
                    profit_mean_list.append(profit_mean)
                    profit_min_list.append(profit_min)
                    time_max_list.append(time_max)
                    time_mean_list.append(time_mean)
                    time_min_list.append(time_min)
            profit_max_list.append(['' for _ in range(len(model_seq))])
            profit_mean_list.append(['' for _ in range(len(model_seq))])
            profit_min_list.append(['' for _ in range(len(model_seq))])
            time_max_list.append(['' for _ in range(len(model_seq))])
            time_mean_list.append(['' for _ in range(len(model_seq))])
            time_min_list.append(['' for _ in range(len(model_seq))])

        result_path = 'result/profit_max.xlsx'
        wb = xw.Book(result_path)
        sheet_name = data_name + '_' + cm_name
        sheet = wb.sheets[sheet_name]
        sheet.cells(7, "C").value = profit_max_list

        result_path = 'result/profit_mean.xlsx'
        wb = xw.Book(result_path)
        sheet_name = data_name + '_' + cm_name
        sheet = wb.sheets[sheet_name]
        sheet.cells(7, "C").value = profit_mean_list

        result_path = 'result/profit_min.xlsx'
        wb = xw.Book(result_path)
        sheet_name = data_name + '_' + cm_name
        sheet = wb.sheets[sheet_name]
        sheet.cells(7, "C").value = profit_min_list

        result_path = 'result/time_max.xlsx'
        wb = xw.Book(result_path)
        sheet_name = data_name + '_' + cm_name
        sheet = wb.sheets[sheet_name]
        sheet.cells(7, "C").value = time_max_list

        result_path = 'result/time_mean.xlsx'
        wb = xw.Book(result_path)
        sheet_name = data_name + '_' + cm_name
        sheet = wb.sheets[sheet_name]
        sheet.cells(7, "C").value = time_mean_list

        result_path = 'result/time_min.xlsx'
        wb = xw.Book(result_path)
        sheet_name = data_name + '_' + cm_name
        sheet = wb.sheets[sheet_name]
        sheet.cells(7, "C").value = time_min_list