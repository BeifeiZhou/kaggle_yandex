__author__ = 'anna'

from get_items import *

n_validation_days = 22
n_training_days= 25

def Get_user_neighbours(neighbours_file):
    res = {}
    with open(neighbours_file) as neighbours:
        for line in neighbours:
            line = line.strip().split("\t")
            res[int(line[0])] = [int(u) for u in line[1:4]]
    return res

def Get_user_prediction(prediction_file, users):
    with open(prediction_file) as prediction:
        for line in prediction:
            line = line.strip().split('\t')
            users[int(line[0])][int(line[1])] = int(line[2])

def Get_users_clicked_urls(prediction_file, users):
    with open(prediction_file) as prediction:
        for line in prediction:
            line = line.strip().split('\t')
            users[int(line[0])].append(int(line[2]))
    for u in users.keys():
        users[u] = set(users[u])


def Get_result(data_file, users_prediction, query_navigatonal):
    user_history = {}
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1

    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**4 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 != 0):
                user_clicks.append([int(line[4]), int(line[5]), int(line[6])])
            else:

                if(len(user_clicks) > 0 and int(line[3]) < n_training_days):
                    if (int(query_id) not in user_history):
                        user_history[int(query_id)] = 0
                    user_history[int(query_id)] += 1

                if (user_id != int(line[0])):
                    n_queries = sum(user_history[u] for u in user_history.keys())
                    navigational_probability = 1./ (n_queries + 1.)
                    if user_id in users_prediction:
                        n_navig = 0
                        for q in users_prediction[user_id]:
                            n_navig += user_history[q]
                        navigational_probability = float(n_navig) / (n_queries+1e-10)
                    for q in user_history:
                        query_navigatonal[q].probability += float(user_history[q]) * navigational_probability
                        query_navigatonal[q].len += user_history[q]

                    user_history = {}
                user_clicks = [[int(line[4]), int(line[5]), int(line[6])]]
                query_id = int(line[2])
                user_id = int(line[0])
                day = int(line[3])

class Query_stat:
    def __init__(self):
        self.probability = 0
        self.len = 0

def main():
    data_file = "../../big_data/trainW2V_medium"
    users_name = Get_users(data_file)

    users = {}
    for u in users_name:
        users[u] = {}
    Get_user_prediction("../../data/query_prediction", users)

    query_names = Get_queries(data_file)
    query_navigatonal = {}
    for q in query_names:
        query_navigatonal[q] = Query_stat()
    Get_result(data_file, users, query_navigatonal)

    with open("../../data/query_navigational", 'w') as res:
        for q in query_navigatonal.keys():
            res.write(str(q) + "\t" + str(query_navigatonal[q].probability / (query_navigatonal[q].len + 1e-10)) + "\n")

main()


