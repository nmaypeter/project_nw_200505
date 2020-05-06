from scipy import stats
from dict import *
import numpy as np


def safe_div(x, y):
    if y == 0:
        return 0.0
    return round(x / y, 4)


class Initialization:
    def __init__(self, data_key, prod_key, cas_key, wallet_key):
        self.data_name = dataset_name_dict[data_key]
        self.data_degree_path = 'data/' + self.data_name + '/degree.txt'
        self.data_weight_path_dict = {
            'ic': 'data/' + self.data_name + '/weight_ic.txt',
            'wc': 'data/' + self.data_name + '/weight_wc.txt'
        }
        self.prod_key = prod_key
        self.cas_key = cas_key
        self.wallet_key = wallet_key
        self.wallet_dict_path = 'data/' + self.data_name + '/wallet_' + product_name_dict[prod_key] + '_' + \
                                wallet_distribution_type_dict[wallet_key] + '.txt'

    def constructSeedCostDict(self):
        # -- calculate the cost for each seed --
        seed_cost_dict, deg_dict = {}, {}
        max_deg = 0
        with open(self.data_degree_path) as f:
            for line in f:
                (node, degree) = line.split()
                max_deg = max(max_deg, int(degree))
                deg_dict[node] = int(degree)
        f.close()

        for i in deg_dict:
            seed_cost_dict[i] = safe_div(deg_dict[i], max_deg)

        return seed_cost_dict

    def constructGraphDict(self):
        # -- build graph --
        ### graph: (dict) the graph
        ### graph[node1]: (dict) the set of node1's receivers
        ### graph[node1][node2]: (float) the weight one the edge of node1 to node2
        path = self.data_weight_path_dict[cascade_model_dict[self.cas_key]]
        graph = {}
        with open(path) as f:
            for line in f:
                (node1, node2, wei) = line.split()
                if node1 in graph:
                    graph[node1][node2] = float(wei)
                else:
                    graph[node1] = {node2: float(wei)}
        f.close()

        return graph

    def constructProductList(self):
        # -- get product list --
        ### prod_list: (list) [profit, cost, price]
        prod_list = p_dict[self.prod_key]
        epw_list = epw_dict[self.wallet_key]

        return prod_list, epw_list

    def constructWalletDict(self):
        # -- get wallet_list from file --
        wallet_dict = {}
        with open(self.wallet_dict_path) as f:
            for line in f:
                (node, wal) = line.split()
                wallet_dict[node] = float(wal)
        f.close()

        return wallet_dict