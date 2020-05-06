model_dict = {
    'method': ['', 'dag1', 'dag2', 'spbp1', 'spbp2', 'ng', 'hd', 'r', 'pmis', 'bcs'],
    'r': ['', 'r'],
    'epw': ['', 'epw']
}


def get_model_name(mn_list):
    model_name = 'm' + model_dict['method'][mn_list[0]] + model_dict['r'][mn_list[1]] + model_dict['epw'][mn_list[2]]

    return model_name


dataset_name_dict = {
    0: 'toy2',
    1: 'email',
    2: 'dnc',
    3: 'Eu',
    4: 'Net',
    5: 'Wiki'
}

product_name_dict = {
    1: 'lphc',
    2: 'hplc'
}

p_dict = {
    1: [
        [0.13, 0.11, 0.24],
        [0.26, 0.22, 0.48],
        [0.39, 0.33, 0.72]
    ],
    2: [
        [0.05, 0.19, 0.24],
        [0.10, 0.38, 0.48],
        [0.15, 0.57, 0.72]
    ]
}

cascade_model_dict = {
    1: 'ic',
    2: 'wc'
}

wallet_distribution_type_dict = {
    0: '',
    1: 'm50e25',
    2: 'm66e34',
    3: 'm99e96'
}

epw_dict = {
    0: [1.0, 1.0, 1.0],
    1: [0.75, 0.5, 0.25],
    2: [0.892, 0.66, 0.34],
    3: [0.9911, 0.9803, 0.9599]
}