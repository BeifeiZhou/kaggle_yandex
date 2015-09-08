import sys
from math import sqrt,exp

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
            g_i = p-truth
            z_i = float(self.get_value_in_dictionary(i, self.z))
            n_i = float(self.get_value_in_dictionary(i, self.n))
            s_i = (sqrt(n_i+g_i**2) - sqrt(n_i)) / self.a
            self.z[i] = z_i + g_i - s_i*w[i]
            self.n[i] = n_i + g_i**2

    def res(self, example):
        features = self.compute_feaatures(example)
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
        res += x_i*y[x_i]
    return res

def HashFeatures(features, feature_names,n_bins):
    hash_features = []
    for i,f in enumerate(features):
        h_f = abs((hash(feature_names[i] + "___" + str(f)) % n_bins)) + 1
        hash_features.append(h_f)
    return hash_features

class Train_model(object):
    def __init__(self, train_file, my_test_file, test_file):
        self.train = open(train_file)
        self.my_test = open(my_test_file)
        self.test = open(test_file)
        self.learner = Linear_regression(0.1,1.,1.,1.)

    def train_by_one_file(self, file_index):
        file = self.train
        if (file_index == 1):
            file = self.test
        for i,line in enumerate(file):
            if (i%10**5 == 0):
                print(i)
            line = line.strip().split('\t')
            ex = [int(feature) for feature in line[:-1]]
            ex.sort()
            truth = float(line[-1] >= 0)
            self.learner.one_step(ex, truth)
        file.close()

    def trainer(self):
        self.train_by_one_file(0)
        self.train_by_one_file(1)

    def test(self, test_file):
        session = []
        session_id = ''
        with open(test_file, 'w') as res_file:
            res_file.write("SessionID,URLID\n")
            for line in self.test:
                line = line.strip().split('\t')
                if len(line[0].split('_')) > 1:
                    if (len(session) > 0):
                        results = []
                        for s in session:
                            results.append([s[0], self.learner.res(s[1])])
                        results.sort(key=lambda x:-x[1])
                        for r in results:
                            res_file.write(r[0]+"\n")
                    session = []
                    if (len(line) > 1):
                        session.append([line[1],[int(i) for i in line[2:-1]]])
                else:
                    session.append([line[0], [int(i) for i in line[1:-1]]])

tr = Train_model("../../data/my_train", "../../data/my_test", "../../data/real_test_1")
tr.trainer()
tr.test("../../data/res")



