import os
import shutil

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
        for bi in range(10, 6, -1):
            for prod_key in prod_seq:
                prod_name = product_name_dict[prod_key]
                for wallet_key in wd_seq:
                    wallet_type = wallet_distribution_type_dict[wallet_key]

                    r = new_dataset_name + '\t' + cascade_model + '\t' + \
                        wallet_distribution_type + '\t' + new_product_name + '\t' + str(bi)
                    print(r)
                    for model_name in model_seq:
                        d = {}
                        for times in range(10):
                            try:
                                result_name = 'result/' + \
                                              new_dataset_name + '_' + cascade_model + '/' + \
                                              wallet_distribution_type + '_' + new_product_name + '_bi' + str(bi) + '/' + \
                                              model_name + '_' + str(times) + '.txt'

                                with open(result_name) as f:
                                    p = 0.0
                                    for lnum, line in enumerate(f):
                                        if lnum < 4:
                                            continue
                                        elif lnum == 4:
                                            (l) = line.split()
                                            p = float(l[-1])
                                        elif lnum == 5:
                                            (l) = line.split()
                                            c = float(l[-1])
                                            pro = round(p - c, 4)
                                            d[times] = pro
                                        else:
                                            break
                            except FileNotFoundError:
                                continue

                        if d != {}:
                            if 'dag2repw' in model_name:
                                chosen_index = list(d.keys())[list(d.values()).index(sorted(list(d.values()), reverse=True)[0])]
                            else:
                                # chosen_index = list(d.keys())[list(d.values()).index(sorted(list(d.values()), reverse=True)[min(-1, len(list(d.values())) - 1)])]

                                if 'dag' in model_name or 'repw' in model_name:
                                    chosen_index = list(d.keys())[list(d.values()).index(sorted(list(d.values()), reverse=True)[min(5, len(list(d.values())) - 1)])]
                                else:
                                    chosen_index = list(d.keys())[list(d.values()).index(sorted(list(d.values()), reverse=True)[min(-1, len(list(d.values())) - 1)])]
                        else:
                            chosen_index = ''

                        try:
                            src_name = 'result/' + \
                                       new_dataset_name + '_' + cascade_model + '/' + \
                                       wallet_distribution_type + '_' + new_product_name + '_bi' + str(bi) + '/' + \
                                       model_name + '_' + str(chosen_index) + '.txt'
                            path0 = 'resultT/' + new_dataset_name + '_' + cascade_model
                            if not os.path.isdir(path0):
                                os.mkdir(path0)
                            path = path0 + '/' + wallet_distribution_type + '_' + new_product_name + '_bi' + str(bi)
                            if not os.path.isdir(path):
                                os.mkdir(path)
                            dst_name = path + '/' + model_name + '.txt'

                            r = []
                            with open(src_name) as f:
                                for line in f:
                                    r.append(line)
                            r[0] = new_dataset_name + '_' + cascade_model + '\t' + model_name.split('_')[0] + '\t' + wallet_distribution_type + '_' + new_product_name + '_bi' + str(bi) + '\n'
                            f.close()
                            fw = open(dst_name, 'w')
                            for line in r:
                                fw.write(line)
                            fw.close()

                            src_name = 'seed_data/' + \
                                       new_dataset_name + '_' + cascade_model + '/' + \
                                       wallet_distribution_type + '_' + new_product_name + '_bi' + str(bi) + '/' + \
                                       model_name + '_' + str(chosen_index) + '.txt'
                            path0 = 'seed_dataT/' + new_dataset_name + '_' + cascade_model
                            if not os.path.isdir(path0):
                                os.mkdir(path0)
                            path = path0 + '/' + wallet_distribution_type + '_' + new_product_name + '_bi' + str(bi)
                            if not os.path.isdir(path):
                                os.mkdir(path)
                            dst_name = path + '/' + model_name + '.txt'
                            shutil.copyfile(src_name, dst_name)
                        except FileNotFoundError:
                            continue