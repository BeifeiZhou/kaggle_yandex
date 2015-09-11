import sys
from math import sqrt,exp
import random

class Linear_regression(object):
    def __init__(self, a, b, l1, l2):
        self.a = a
        self.b = b
        self.l1 = l1
        self.l2 = l2
        self.z = {}
        self.n = {}

    def compute_features(self, example):
        return example

    def get_value_in_dictionary(self, i, dic):
        res = 0
        if i in dic:
           res = dic[i]
        return res

    def get_w(self, features):
        w = {}
        for i in features:
            w[i] = 0

            z_i = float(self.get_value_in_dictionary(i, self.z))
            n_i = float(self.get_value_in_dictionary(i, self.n))

            if (abs(z_i) > self.l1):
                w[i] = -((self.b+sqrt(n_i))/self.a + self.l2)**-1
                w[i] *= z_i - Sgn(z_i)*self.l1
        return w

    def one_step(self, example, truth):
        # features is a list of indexis of non zero features
        features = self.compute_features(example)
        w = self.get_w(features)
        p = Sigmoid(Scalar_product(features, w))
        for i in features:
            if (random.randint(0,5) == 0):
                g_i = p-truth
                z_i = float(self.get_value_in_dictionary(i, self.z))
                n_i = float(self.get_value_in_dictionary(i, self.n))
                s_i = (sqrt(n_i+g_i**2) - sqrt(n_i)) / self.a
                self.z[i] = z_i + g_i - s_i*w[i]
                self.n[i] = n_i + g_i**2

    def res(self, example):
        features = self.compute_features(example)
        w = self.get_w(features)
        return Sigmoid(Scalar_product(features,w))


def Sigmoid(x):
    return 1./(1. + exp(-x))

def Sgn(x):
    if (x > 0):
        return 1.
    return -1

def Scalar_product(x,y):
    res = 0
    for x_i in x:
        res += y[x_i]
    return res

def HashFeatures(features, feature_names,n_bins):
    hash_features = []
    for i,f in enumerate(features):
        h_f = abs((hash(feature_names[i] + "___" + str(f)) % n_bins)) + 1
        hash_features.append(h_f)
    return hash_features





