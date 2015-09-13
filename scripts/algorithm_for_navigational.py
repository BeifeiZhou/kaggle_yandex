import sys

def Get_prediction(user_query_train, query, user_clicks):
    basic_prediction = user_clicks[0][0]
    prediction = basic_prediction
    make_predictions = 0
    n_right_actually_prediction_navigation = 0
    if(query in user_query_train and user_query_train[query].len >= 2):
        prediction = user_query_train[query].prediction
        make_predictions = 1
    a = [i[1] for i in user_clicks if i[0] == prediction]
    if (a == []):
        prediction_type = user_clicks[0][1]
    else:
        prediction_type = a[0]
    navigational, basic = 0,0
    truth = max([user_clicks[i][1] for i in range(len(user_clicks))])
    if (truth == prediction_type):
        navigational = 1
        if (make_predictions > 0):
            n_right_actually_prediction_navigation = 1
    if (truth == user_clicks[0][1]):
        basic = 1
    return [navigational, basic, make_predictions, n_right_actually_prediction_navigation]

class query_statistic:
    def __init__(self):
        self.prediction = -1
        self.len = 0

def Get_users_for_queries(data_file):
    #res_navigational = open(res_file_navigational, 'w')
    #res_basic = open(res_file_basic, 'w')
    user_id = 0
    query = 0
    day = 0
    user_clicks = []
    user_query_train = {}
    n_all_queries = 0
    n_right_prediction_basic = 0
    n_right_prediction_navigation = 0
    n_predictions = 0
    n_right_actually_prediction_navigation = 0
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (not line_n%10 == 0):
                user_clicks.append([int(line[-3]), int(line[-2]), int(line[-1])])

            if (line_n%10 == 0 and len(user_clicks) > 0):
                user_clicks.sort(key=lambda x: x[-1])
                if (day >= 25):
                    navigational, basic, prediction_done, actually_prediction_navigation = \
                        Get_prediction(user_query_train, query, user_clicks)
                    n_all_queries += 1
                    n_right_prediction_navigation += navigational
                    n_right_prediction_basic += basic
                    n_predictions += prediction_done
                    n_right_actually_prediction_navigation += actually_prediction_navigation
                else:
                    truth = max([user_clicks[i][1] for i in range(len(user_clicks))])
                    if (truth >= 0):
                        prediction = [i[0] for i in user_clicks if i[1] == truth]
                        if (query not in user_query_train):
                            user_query_train[query] = query_statistic()
                        if len(prediction) >= 2:
                            user_query_train[query] = query_statistic()
                        else:
                            if (user_query_train[query].len >= 1 and
                                        user_query_train[query].prediction == prediction[0]):
                                user_query_train[query].len += 1
                            else:
                                user_query_train[query].len = 1
                                user_query_train[query].prediction = prediction[0]
            if (line_n%10 == 0):
                user_clicks = [[int(line[-3]), int(line[-2]), int(line[-1])]]
                query = line[2]
                day = int(line[3])
                if (user_id != line[0]):
                    user_id = line[0]
                    user_query_train = {}
    print ("Basic result = " + str(n_right_prediction_basic) + "," + str(n_all_queries) + "\t" + str(float(n_right_prediction_basic)/n_all_queries))
    print ("Navigational result = " + str(n_right_prediction_navigation) + "," + str(n_all_queries) +
           "\t" + str(float(n_right_actually_prediction_navigation)/n_predictions)+"\t" + str(float(n_right_prediction_navigation)/n_all_queries))

Get_users_for_queries("../../data/trainW2V")