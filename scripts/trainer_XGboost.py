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
            t = int(line[-1])
            truth = 0
            #if (t == -1):
            #    truth = 0.
            if (t == 2):
                truth = 1.
           # truth = float(int(line[-1]) >= 2)
            if (truth >= 0):
                res.append(ex)
                labels.append(truth)
    return [res, labels]

def Train(train, validation):
    dtrain = xgb.DMatrix(np.array(train[0]), label=np.array(train[1]))
    dvalidation = xgb.DMatrix(validation[0], label = np.array(validation[1]))
    eval_set  = [(train[0],train[1]), (validation[0],validation[1])]
    gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05, silent=True
                            ).fit(train[0], train[1] ,eval_set= eval_set, early_stopping_rounds=40)

    return gbm


def Best_permutation(x,y):
    for i in range(len(x)):
        if (x[i] > y[i]):
            return 1
        if (x[i] < y[i]):
            return -1
    return 0

def Get_prediction_permutation(prediction, labels):
    pr = [[max(float(prediction[i]),0), i] for i in range(len(prediction))]
    pr.sort(key=lambda x: [-x[0],x[1]])
    return [labels[pr[i][1]] for i in range(len(pr))]

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
                if (line_n > 1*10**6):
                    break
                line = line.strip().split('\t')
                if (len(session)%10 == 0):
                    if (len(session) > 0):
                        session = np.array(session)
                        predictions = session[0][0:10]
                        answer = Best_permutation(Get_prediction_permutation(predictions, labels), labels)
                        if (answer > 0 and max(predictions) > 5):
                            n_right_actually_prediction += 1
                        if (answer < 0 and max(predictions) > 5):
                            n_predictions += 1
                            res.write("\t".join(str(s) for s in list(predictions)) + "\n")
                            res.write("\t".join(str(l) for l in labels) + "\n\n")

                    session = []
                    labels = []
                    rangs = []
                    if (len(line) > 1):
                        try:
                            session.append([float(i) for i in line[:-1]])
                            labels.append(float(line[-1]))
                            rangs.append(int(line[-2]))
                        except:
                            break
                else:
                    try:
                        label = float(line[-1])
                        if (label < 0):
                            label = -1
                        session.append([float(i) for i in line[:-1]])
                        labels.append(label)
                        rangs.append(int(line[-2]))
                    except:
                        break

        return [correct_answer, n_answers,  n_right_actually_prediction, n_predictions]

def main():
    #train_data = Load_data("../../data/validation")
    #test_data = Load_data("../../data/testForIdea")
    gbm = 1
    #gbm = Train(train_data, test_data)
    #gbm.save_model('my.model')
    #gbm.dump_model('dump.raw.txt', 'featmap.txt')
    print(run_test("../../big_data/trainW2V_small_test_q", gbm))
    #print(run_test("../../data/validation", gbm))

main()
