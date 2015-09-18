__author__ = 'anna'

import xgboost as xgb
import numpy as np

def Load_data(data_file):
    res = []
    labels = []
    with open(data_file) as file:
        for i,line in enumerate(file):
            if (i%10**6 == 0):
                print(i)
            line = line.strip().split('\t')
            ex = [float(feature) for feature in line[:-1]]
            truth = float(int(line[-1]) >= 2)
            res.append(ex)
            labels.append(truth)
    return [res, labels]

def Train(train):
    dtrain = xgb.DMatrix(np.array(train[0]), label=np.array(train[1]))
    gbm = xgb.XGBClassifier(max_depth=1, n_estimators=1000, learning_rate=0.05).fit(train[0], train[1])

    return gbm

def run_test(test_file, gbm):
        session = []
        labels = []
        rangs = []
        correct_answer = 0
        n_answers = 0
        n_predictions = 0
        n_right_actually_prediction = 0
        with open(test_file) as test, open("../../data/res", 'w') as res:
            for line_n,line in enumerate(test):
                if (line_n%10**4 == 0):
                    print(line_n)
                line = line.strip().split('\t')
                #if len(line[0].split('_')) > 1:
                if (line_n%10 == 0):
                    if (len(session) > 0):
                        session = np.array(session)
                        #truth = np.array(labels)
                        predictions = gbm.predict(session)
                        if (max(predictions) > 0):
                            res.write("\t".join(str(i) for i in predictions) + "\n")
                            res.write("\t".join(str(i) for i in labels) + "\n\n")
                            p = [i for i in range(len(predictions)) if predictions[i] > 0]
                            if (labels[p[0]] == max(labels)):
                                n_right_actually_prediction += 1
                            n_predictions += 1


                        results = []
                        for i in range(len(labels)):
                            results.append([rangs[i], predictions[i], labels[i]])
                        results.sort(key=lambda x:-x[1])
                        urls_with_max_score = [r for r in results if abs(r[1] - results[0][1]) < 1e-10]
                        urls_with_max_score.sort(key = lambda x:x[0])
                        max_truth = max(r[2] for r in results)
                        if (int(max_truth) == int(urls_with_max_score[0][2])):
                            correct_answer += 1
                        n_answers += 1
                    session = []
                    labels = []
                    rangs = []
                    if (len(line) > 1):
                        session.append([float(i) for i in line[:-1]])
                        labels.append(float(line[-1]))
                        rangs.append(line_n%10)
                else:
                    session.append([float(i) for i in line[:-1]])
                    labels.append(float(line[-1]))
                    rangs.append(line_n%10)
        return [correct_answer, n_answers,  n_right_actually_prediction, n_predictions]

def main():
    train_data = Load_data("../../my_data/validation_new")
    gbm = Train(train_data)
    #gbm.save_model('my.model')
    #gbm.dump_model('dump.raw.txt', 'featmap.txt')
    print(run_test("../../my_data/test_new", gbm))
    print(run_test("../../my_data/validation_new", gbm))

main()