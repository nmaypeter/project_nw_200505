from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import math


def generateDistribution(price_list, m, e):
    counter, counter_flag, temp_counter, temp_mu, temp_sigma = 0, True, 100.0, 0, 1.0

    mu = m
    sigma = abs(m - e)

    X = np.arange(0, 2, 0.001)
    Y = stats.norm.sf(X, mu, sigma)
    product_weight_list = [round(float(Y[np.argwhere(X == p)]), 4) for p in price_list]

    alpha, beta = 0.0, 1.0
    while (str(product_weight_list[1]) != str(m) or str(product_weight_list[2]) != str(e)) and counter_flag:
        # print(product_weight_list, alpha, beta, counter)
        if (abs(product_weight_list[1] - m) >= 0.01) or (abs(product_weight_list[2] - e) >= 0.01):
            if abs(product_weight_list[1] - m) >= 0.01:
                alpha = alpha + 0.01 if product_weight_list[1] > m else alpha - 0.01
                beta = beta + 0.0001 if product_weight_list[2] > e else beta - 0.0001
            elif abs(product_weight_list[2] - e) >= 0.01:
                alpha = alpha + 0.0001 if product_weight_list[1] > m else alpha - 0.0001
                beta = beta + 0.01 if product_weight_list[2] > e else beta - 0.01
        else:
            alpha = alpha + 0.0001 if product_weight_list[1] > m else alpha - 0.0001
            beta = max(beta + 0.0001 if product_weight_list[2] > e else beta - 0.0001, 0.0001)

        mu = m - alpha
        sigma = abs(m - e) / beta
        Y = stats.norm.sf(X, mu, sigma)
        product_weight_list = [round(float(Y[np.argwhere(X == p)]), 4) for p in price_list]

        if abs(product_weight_list[1] - m) <= 0.05 and abs(product_weight_list[2] - e) <= 0.05:
            counter += 1
            if counter >= 1000:
                counter_flag = False
            if abs(product_weight_list[1] - m) + abs(product_weight_list[2] - e) <= temp_counter:
                temp_counter = abs(product_weight_list[1] - m) + abs(product_weight_list[2] - e)
                temp_mu, temp_sigma = mu, sigma

        if True in [math.isnan(i) for i in product_weight_list]:
            alpha, beta = 0.0, 1.0
            mu = np.mean(price_list)
            sigma = 0.001
            Y = stats.norm.sf(X, mu, sigma)
            product_weight_list = [round(float(Y[np.argwhere(X == p)]), 4) for p in price_list]

    if counter == 1000:
        mu, sigma = temp_mu, temp_sigma

    Y = stats.norm.sf(X, mu, sigma)
    product_weight_list = [round(float(Y[np.argwhere(X == p)]), 4) for p in price_list]

    return mu, sigma


if __name__ == '__main__':
    price_list_g = [0.24, 0.48, 0.72]
    m_g = 0.50
    e_g = 0.1
    wd_g = 'm' + str((int(m_g * 100))) + 'e' + str(int(e_g * 100))
    print(wd_g)

    mu_g, sigma_g = generateDistribution(price_list_g, m_g, e_g)
    X_g = np.arange(0, 2, 0.001)
    Y_g = [stats.norm.pdf(X_g, mu_g, sigma_g), stats.norm.cdf(X_g, mu_g, sigma_g), stats.norm.sf(X_g, mu_g, sigma_g)]

    product_weight_list_g = [round(float(Y_g[2][np.argwhere(X_g == p)]), 4) for p in price_list_g]
    print(product_weight_list_g)
    print(round(float(stats.norm.sf(price_list_g[0] + price_list_g[1], mu_g, sigma_g)), 4))
    print(round(float(stats.norm.sf(price_list_g[0] + price_list_g[2], mu_g, sigma_g)), 4))
    print(round(float(stats.norm.sf(price_list_g[1] + price_list_g[2], mu_g, sigma_g)), 4))
    print(round(float(stats.norm.sf(sum(price_list_g), mu_g, sigma_g)), 4))

    # -- plot --
    X_label = ['wallet guess', 'wallet guess', 'number of nodes with purchasing ability guess']
    Y_label = ['probability density', 'probability', 'probability']
    title = ['pdf', 'cdf', 'ccdf']

    for index in range(3):
        plt.plot(X_g, Y_g[index])
        plt.xlabel(X_label[index])
        plt.ylabel(Y_label[index])
        plt.title(title[index] + ' of wd: ' + wd_g + ': μ = ' + str(round(mu_g, 4)) + ', σ = ' + str(round(sigma_g, 4)))
        plt.grid()
        save_name = 'distribution/' + wd_g + '_' + title[index]
        plt.savefig(save_name)
        plt.show()