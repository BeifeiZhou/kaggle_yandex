import sys
from urls_as_summ_urls import *

def Get_navigetional(nav_file):
    res = {}
    with open(nav_file) as nav:
        for line in nav:
            line = line.strip().split("\t")
            res[int(line[0])] = float(line[1])
    return res

def Get_prediction(user_prediction, query, user_clicks):
    basic_prediction = user_clicks[0][0]
    prediction = basic_prediction
    make_predictions = 0
    n_right_actually_prediction_navigation = 0
    urls = set(u[0] for u in user_clicks).intersection(user_prediction)
    if(len(urls) > 0):
    #if(user_id in user_prediction and query in user_prediction[user_id]):
        #prediction = user_prediction[user_id][query]
        for u in urls:
            prediction = u
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

def Get_users_for_queries(data_file, urls_vector, users_vector_as_urls):
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

    lines = []
    with open(data_file) as data :#, open("../../data/query_prediction", 'w') as n_train:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line1 = line
            line = line.strip().split("\t")
            if (not line_n%10 == 0):
                user_clicks.append([int(line[-3]), int(line[-2]), int(line[-1])])
                #lines.append(line1.strip())

            if (line_n%10 == 0 and len(user_clicks) > 0):
                user_clicks.sort(key=lambda x: x[-1])
                if (day < 25 and day >= 22):
                    user_prediction = []
                    for q in user_query_train:
                        user_prediction.append(user_query_train[q].prediction)
                    user_prediction = set(user_prediction)
                    if (sum(np.inner(urls_vector[int(u[0])], users_vector_as_urls[int(user_id)])
                            for u in user_clicks) < 0.05 and
                            max(int(u[1]) for u in user_clicks) > 1):
                        navigational, basic, prediction_done, actually_prediction_navigation = \
                            Get_prediction(user_prediction, query, user_clicks)
                        n_all_queries += 1
                        n_right_prediction_navigation += navigational
                        n_right_prediction_basic += basic
                        n_predictions += prediction_done
                        n_right_actually_prediction_navigation += actually_prediction_navigation
                    #if (prediction_done < 1):
                    #    n_train.write("\n".join(l for l in lines) + "\n")
                elif(day < 22):
                    #n_train.write("\n".join(l for l in lines) + "\n")
                    truth = max([user_clicks[i][1] for i in range(len(user_clicks))])
                    if (truth >= 0):
                        prediction = [i[0] for i in user_clicks if i[1] == truth]
                        if (query not in user_query_train):
                            user_query_train[query] = query_statistic()

                        if len(prediction) >= 2:
                            user_query_train[query] = query_statistic()
                            user_query_train[query].prediction == prediction[-1]
                            user_query_train[query].len = 1
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
		#lines = [line1.strip()]
                if (user_id != line[0]):
                    #for q in user_query_train.keys():
                    #    if(user_query_train[q].len >= 2):
                    #        n_train.write(str(user_id) + "\t" + str(q) + "\t" + str(user_query_train[q].prediction) + "\n")
                    user_id = line[0]
                    user_query_train = {}
    print ("Basic result = " + str(n_right_prediction_basic) + "," + str(n_all_queries) + "\t" + str(float(n_right_prediction_basic)/n_all_queries))
    print ("Navigational result = " + str(n_right_prediction_navigation) + "," + str(n_all_queries) +
           "\t" + str(n_right_actually_prediction_navigation) + "\t" + str(n_predictions)+"\t" + str(float(n_right_prediction_navigation)/n_all_queries))

def main():
    data_file = "../../big_data/trainW2V_small_q"
    #navigational = Get_navigetional("../../data/query_navigational")

    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)


    urls_vector = get_features(urls_name, dim)
    users_vector_as_urls = users_as_sum_urls(data_file, urls_vector, users_name)

    Get_users_for_queries(data_file, urls_vector, users_vector_as_urls)





main()
