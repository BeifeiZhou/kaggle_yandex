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

def Get_prediction( query, user_clicks, user_prediction, user_id):
    basic_prediction = user_clicks[0][0]
    prediction = basic_prediction
    make_predictions = 0
    n_right_actually_prediction_navigation = 0

    urls = set()
    if (user_id in user_prediction):
        urls = set(u[0] for u in user_clicks).intersection(user_prediction[user_id])
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

def Get_users_for_queries(data_file, users_prediction):

    user_id = 0
    query = 0
    day = 0
    user_clicks = []
    n_all_queries = 0
    n_right_prediction_basic = 0
    n_right_prediction_navigation = 0
    n_predictions = 0
    n_right_actually_prediction_navigation = 0
    lines = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line1 = line
            line = line.strip().split("\t")
            if (not line_n%10 == 0):
                user_clicks.append([int(line[-3]), int(line[-2]), int(line[-1])])

            if (line_n%10 == 0 and len(user_clicks) > 0):
                user_clicks.sort(key=lambda x: x[-1])
                if (day >= 25):
                    navigational, basic, prediction_done, actually_prediction_navigation = \
                        Get_prediction(query, user_clicks, users_prediction, user_id)
                    n_all_queries += 1
                    n_right_prediction_navigation += navigational
                    n_right_prediction_basic += basic
                    n_predictions += prediction_done
                    n_right_actually_prediction_navigation += actually_prediction_navigation

            if (line_n%10 == 0):
                user_clicks = [[int(line[-3]), int(line[-2]), int(line[-1])]]
                query = int(line[2])
                day = int(line[3])
                if (user_id != int(line[0])):
                    user_id = int(line[0])

    print ("Basic result = " + str(n_right_prediction_basic) + "," + str(n_all_queries) + "\t" + str(float(n_right_prediction_basic)/n_all_queries))
    print ("Navigational result = " + str(n_right_prediction_navigation) + "," + str(n_all_queries) +
           "\t" + str(n_right_actually_prediction_navigation) + "\t" + str(n_predictions)+"\t" + str(float(n_right_prediction_navigation)/n_all_queries))

def One_step_expander(users_neighbours, users):
    users_prediction = {}
    for u in users.keys():
        users_prediction[u] = {}
        for q in users[u].keys():
            users_prediction[u][q] = users[u][q]

    for u in users_neighbours.keys():
        for friend in users_neighbours[u]:
            for q in users[friend].keys():
                if q not in users_prediction[u].keys():
                    users_prediction[u][q] = users[friend][q]
    return users_prediction

def One_step_expander_by_urls(users_neighbours, users):
    users_prediction = {}
    for u in users_neighbours.keys():
        users_prediction[u] = list(users[u])
        for friend in users_neighbours[u]:
            if (friend in users.keys()):
                users_prediction[u] += users[friend]
        users_prediction[u] = set(users_prediction[u])
    return users_prediction

def main():
    data_file = "../../data/trainW2V"
    users_name = Get_users(data_file)

    users_neighbours = Get_user_neighbours("../../data/users_neighbours")
    users = {}
    for u in users_name:
        users[u] = []
    #Get_user_prediction("../../data/query_prediction", users)
    Get_users_clicked_urls("../../data/query_prediction", users)

    n_steps = 2
    for i in range(n_steps):
        print(i)
        users = One_step_expander_by_urls(users_neighbours, users)


    Get_users_for_queries(data_file, users)

main()
