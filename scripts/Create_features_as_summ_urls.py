__author__ = 'anna'
from W2V import *


dim = 300
n_validation_days = 22
n_trainig_days_ = 25
c_q = 0.95

def Get_features(queries_name):
    res = {}
    for q in queries_name:
        res[q] = Get_random_vector(dim)
    return res

def Get_queries_features(data_file, users_features, query_names):
    res = {}
    for q in query_names:
        res[q] = [0 for i in range(dim)]
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n % 10 == 0 and int(line[3]) < n_validation_days):
                for i in range(dim):
                    weight = c_q**(n_trainig_days_ - int(line[3]))
                    res[int(line[2])][i] += users_features[int(line[0])][i]
    return res

def Get_url_features(data_file, users_features, urls_names):
    res = {}
    for u in urls_names:
        res[u] = [0 for i in range(dim)]
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (int(line[5]) == 2 and int(line[3]) < n_validation_days):
                for i in range(dim):
                    weight = c_q**(n_trainig_days_ - int(line[3]))
                    res[int(line[4])][i] += users_features[int(line[0])][i]
    return res

def Get_new_features_for_query(data_file, queries_name):
    res = {}
    for q in queries_name:
        res[q] = []
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 != 0):
                user_clicks.append([int(line[4]), int(line[5])])
            else:
                if (len(user_clicks) > 0 and day >= n_trainig_days_ - 21 and day < n_trainig_days_):
                    truth = max (u[1] for u in user_clicks)
                    if (truth == 2):
                        clicks = [u[0] for u in user_clicks if u[1] == truth]
                        for c in clicks:
                            for url in clicks:
                                res[query_id].append([url, user_id, day])
                user_clicks = [[int(line[4]), int(line[5])]]
                query_id = int(line[2])
                user_id = int(line[0])
                day = int(line[3])
    return res