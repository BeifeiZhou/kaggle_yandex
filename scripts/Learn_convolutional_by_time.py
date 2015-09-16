__author__ = 'annasepliaraskaia'

from sklearn import linear_model


def Get_truth(truth):
    if truth == "True":
        return 1
    return 0

def Get_data(data_file):
    samples = []
    truth = []
    with open(data_file) as data:
        for line in data:
            line = line.strip().split("\t")
            features = [0. for i in range(3)]
            n_nol_zero = 0
            i = 0
            while n_nol_zero < 3 and i < len(line)-1:
                if (float(line[i]) > 0):
                    features[n_nol_zero] = float(line[i])
                    n_nol_zero += 1
                i += 1
            samples.append(features)
            truth.append(Get_truth(line[-1]))
    return [samples, truth]

def Learn_linear(samples, truth):
    est = linear_model.LinearRegression()
    est.fit(samples, truth)
    print(est.coef_)




def main():
    samples, truth = Get_data("../../data/for_training")
    Learn_linear(samples, truth)

main()
