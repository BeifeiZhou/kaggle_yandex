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
                if (len(session)%10 == 0):
                    if (len(session) > 0):
                        session = np.array(session)
                        #truth = np.array(labels)
                        #predictions = gbm.predict(session)
                        predictions= [0 for i in range(10)]

                        max_counter = max(session[0][0:10])
                        counters = [session[0][i]/(i+1.) for i in range(10)]
                        counters.sort(key=lambda x: -x)
                        max_counter = counters[0]

                        if (counters[0]/counters[1]) > 1.5 and (counters[0] > 5) \
                           and session[0][0] < 15 :
                            s = 0
                            while(max(predictions) < 1 and s < 10):
                                if (session[0][s] / (s+1.) >= max_counter):
                                    predictions[s] = 1
                                s += 1




                        if (max(predictions) > 0 and predictions[0] == 0):

                            p = [i for i in range(len(predictions)) if predictions[i] > 0]
                            if (labels[p[0]] == max(labels)):
                                if (labels[0] != max(labels)):
                                    n_right_actually_prediction += 1
                            elif (labels[0] == max(labels)):
                                res.write("\t".join(str(i) for i in session[0][0:10]) + "\t" + str(line_n) + "\n")
                                res.write("\t".join(str(i) for i in labels)+ "\t" + str(line_n) + "\n\n")
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
                        try:
                            session.append([float(i) for i in line[:-1]])
                            labels.append(float(line[-1]))
                            rangs.append(int(line[-2]))
                        except:
                            break
                else:
                    try:
                        session.append([float(i) for i in line[:-1]])
                        labels.append(float(line[-1]))
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
