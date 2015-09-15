__author__ = 'anna'

from get_items import *
from Create_features_as_summ_urls import *

def Get_query_click_probability(user_history):
    for q in user_history.keys():
        clicks = [[url, user_history[q][url]] for url in user_history[q].keys()]
        clicks_summ = sum([i[1] for i in clicks])
        for url in user_history[q].keys():
            user_history[q][url] /= float(clicks_summ + 1e-10)

def Get_user_prediction(user_history, user_click, query_vector, urls_vector, query):
    query_feature = query_vector[query]
    click_predicion = {}
    for u in user_click:
        click_predicion[u[0]] = 0
    for u in user_click:
        url_feature = urls_vector[u[0]]
        for q in user_history.keys():
            d = Cos(query_feature, query_vector[q])
            if (d > 0.9):
                for url in user_history[q]:
                     d_u = Cos(url_feature, urls_vector[url])
                     if (url == u[0]):
                         click_predicion[u[0]] += d* d_u * user_history[q][url]
    return click_predicion

def Get_result(data_file, urls_vector, query_features):
    user_history = {}
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1
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
            if (line_n%10 != 0):
                user_clicks.append([int(line[4]), int(line[5]), int(line[6])])
            else:
                if (day >= n_trainig_days_ and len(user_clicks) > 0):
                    user_clicks.sort(key = lambda x: x[2])
                    Get_query_click_probability(user_history)
                    click_prediction = Get_user_prediction(user_history, user_clicks, query_features, urls_vector, query_id)
                    navigational, basic, prediction_done, actually_prediction_navigation = \
                        Get_prediction(click_prediction, user_clicks)
                    n_all_queries += 1
                    n_right_prediction_navigation += navigational
                    n_right_prediction_basic += basic
                    n_predictions += prediction_done
                    n_right_actually_prediction_navigation += actually_prediction_navigation

                elif(len(user_clicks) > 0 and int(line[3]) >= n_trainig_days_ - 21):
                    for cl in user_clicks:
                        if (cl[1] == 2):
                            if (int(query_id) not in user_history):
                                user_history[int(query_id)] = {}
                            if (int(cl[0]) not in user_history[int(query_id)]):
                                user_history[int(query_id)][int(cl[0])] = 0
                            user_history[int(query_id)][int(cl[0])] += c_q ** (n_trainig_days_ - day)
                if (user_id != int(line[0])):
                    user_history = {}

                user_clicks = [[int(line[4]), int(line[5]), int(line[6])]]
                query_id = int(line[2])
                user_id = int(line[0])
                day = int(line[3])

    print ("Basic result = " + str(n_right_prediction_basic) + "," + str(n_all_queries) + "\t" + str(float(n_right_prediction_basic)/n_all_queries))
    print ("Navigational result = " + str(n_right_prediction_navigation) + "," + str(n_all_queries) +
           "\t" +str(n_right_actually_prediction_navigation) + "," +str(n_predictions) + "\t" + str(float(n_right_prediction_navigation)/n_all_queries))

def Get_prediction(click_prediction, user_clicks):
    basic_prediction = user_clicks[0][0]
    prediction = basic_prediction
    make_predictions = 0
    n_right_actually_prediction_navigation = 0
    max_click_prediction = max(click_prediction[u] for u in click_prediction.keys())
    sum_prediction = sum(click_prediction[u] for u in click_prediction.keys())
    if(float(max_click_prediction) / (sum_prediction+1e-10) > 0.5):
        prediction = [u for u in click_prediction.keys() if click_prediction[u] == max_click_prediction]
        prediction = prediction[0]
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

def main():
    data_file = "../../data/trainW2V"
    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    users_features = Get_features(users_name)
    urls_vector = Get_url_features(data_file, users_features, urls_name)
    query_features = Get_queries_features(data_file, users_features, queries_name)

    Get_result(data_file, urls_vector, query_features)

main()