from keras.datasets import mnist
import numpy as np
from Interval import Interval
import pandas as pd

(train_X, train_y), (test_X, test_y) = mnist.load_data()

def get_ones(flatten = False):
    ones = []
    for i in range(len(test_X)):
        if train_y[i] == 1:
            ones.append(test_X[i])
    if flatten:
        ones = np.array(ones).reshape(-1, 784)
        return ones
    return ones

def read_csv():
    df = pd.read_csv('ones_mu_sig.csv')
    return np.abs(df['mean'].to_numpy()-255), np.abs(df['std'].to_numpy())

def log_prob(x, mean, sigma):
    return -((x - mean)**2 / (2 * sigma**2)) - np.log(sigma * np.sqrt(2 * np.pi))

def log_prob_comparison(one, means, sigmas, e=5):
    tot_disc_score = 0
    tot_int_score = 0
    assert len(one) == len(means) == len(sigmas) == 784, f"|one| = {len(one)}, |means| = {len(means)}, |sigmas| = {len(sigmas)}"
    for pix, mean, sigma in zip(one, means, sigmas):
        int = Interval(pix-e, pix+e)
        tot_disc_score += log_prob(pix, mean, sigma)
        tot_int_score += log_prob(int, mean, sigma)

    return tot_disc_score, tot_int_score

if __name__ == "__main__":
    ones = get_ones(flatten=True)
    one = ones[0]
    means, sigmas = read_csv()
    res1, res2 = log_prob_comparison(one, means, sigmas)
    print(res1, res2)
