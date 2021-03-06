from generateDistribution import *
from random import choice
from dict import *


def safe_div(x, y):
    if y == 0:
        return 0.0
    return round(x / y, 4)


class IniDataset:
    def __init__(self, data_key):
        ### data_data_path, data_ic_weight_path, data_wc_weight_path, data_degree_path, product_path: (str) tha file path
        self.data_name = dataset_name_dict[data_key]
        self.data_path = 'data/' + self.data_name + '/data.txt'
        self.data_degree_path = 'data/' + self.data_name + '/degree.txt'
        self.data_weight_path_dict = {
            'ic': 'data/' + self.data_name + '/weight_ic.txt',
            'wc': 'data/' + self.data_name + '/weight_wc.txt'
        }

    def setEdgeWeight(self):
        # -- browse dataset --
        out_degree_list, in_degree_list = [], []
        with open(self.data_path) as f:
            for line in f:
                (node1, node2) = line.split()
                out_degree_list.append(node1)
                in_degree_list.append(node2)
        f.close()
        num_node = max([int(i) for i in out_degree_list+in_degree_list])

        # -- count degree for each node --
        fw = open(self.data_degree_path, 'w')
        for i in range(0, num_node + 1):
            fw.write(str(i) + '\t' + str(out_degree_list.count(str(i))) + '\n')
        fw.close()

        ic_graph, wc_graph = {}, {}
        with open(self.data_path) as f:
            for line in f:
                (node1, node2) = line.split()

                if node1 in ic_graph:
                    if node2 in ic_graph[node1]:
                        ic_graph[node1][node2] = 1 - 0.9 * (1 - ic_graph[node1][node2])
                        wc_graph[node1][node2] += safe_div(1, in_degree_list.count(node2))
                    else:
                        ic_graph[node1][node2] = 0.1
                        wc_graph[node1][node2] = safe_div(1, in_degree_list.count(node2))
                else:
                    ic_graph[node1] = {node2: 0.1}
                    wc_graph[node1] = {node2: safe_div(1, in_degree_list.count(node2))}

        ic_graph = {node1: {node2: 1.0 if ic_graph[node1][node2] >= 1.0 else round(ic_graph[node1][node2], 4) for node2 in ic_graph[node1]} for node1 in ic_graph}
        wc_graph = {node1: {node2: 1.0 if wc_graph[node1][node2] >= 1.0 else round(wc_graph[node1][node2], 4) for node2 in wc_graph[node1]} for node1 in wc_graph}

        # -- set weight on edge for ic model and wc model --
        fw_ic = open(self.data_weight_path_dict['ic'], 'w')
        fw_wc = open(self.data_weight_path_dict['wc'], 'w')
        for node1 in ic_graph:
            for node2 in ic_graph[node1]:
                fw_ic.write(node1 + '\t' + node2 + '\t' + str(ic_graph[node1][node2]) + '\n')
                fw_wc.write(node1 + '\t' + node2 + '\t' + str(wc_graph[node1][node2]) + '\n')
        fw_wc.close()
        fw_ic.close()


def getQuantiles(pd, mu, sigma):
    discrimination = -2 * sigma**2 * np.log(pd * sigma * np.sqrt(2 * np.pi))

    # no real roots
    if discrimination < 0:
        return None
    # one root, where x == mu
    elif discrimination == 0:
        return mu
    # two roots
    else:
        return choice([mu - np.sqrt(discrimination), mu + np.sqrt(discrimination)])


class IniWallet:
    def __init__(self, data_key, prod_key, wallet_key):
        self.data_name = dataset_name_dict[data_key]
        self.data_degree_path = 'data/' + self.data_name + '/degree.txt'
        self.prod_key = prod_key
        self.prod_name = product_name_dict[prod_key]
        self.wallet_type = wallet_distribution_type_dict[wallet_key]
        self.wallet_dict_path = 'data/' + self.data_name + '/wallet_' + self.prod_name + '_' + self.wallet_type + '.txt'

    def setNodeWallet(self):
        # -- set wallet for each node for each item --
        price_list = [p[-1] for p in p_dict[self.prod_key]]

        with open(self.data_degree_path) as f:
            for line in f:
                (num_node, degree) = line.split()
        f.close()

        wd = list(self.wallet_type)
        m, e = int(wd[1] + wd[2]), int(wd[4] + wd[5])
        mu, sigma = generateDistribution(price_list, m*0.01, e*0.01)

        fw = open(self.wallet_dict_path, 'w')
        for i in range(0, int(num_node) + 1):
            wal = 0
            while wal <= 0:
                q = stats.norm.rvs(mu, sigma)
                pd = stats.norm.pdf(q, mu, sigma)
                wal = getQuantiles(pd, mu, sigma)
            fw.write(str(i) + '\t' + str(round(wal, 2)) + '\n')
        fw.close()