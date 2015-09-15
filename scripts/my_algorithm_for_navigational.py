from W2V import *

dim = 300
n_trainig_days_ = 25
n_validation_days = 22

def Get_queries(data_file):
    queries_name = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 == 0):
                queries_name.append(line[2])
    return set(queries_name)

def Get_urls(data_file):
    urls_name = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            urls_name.append(int(line[4]))
    return set(urls_name)

def Get_queries_features(queries_name):
    res = {}
    for q in queries_name:
        res[q] = Get_random_vector(dim)
    return res

def Get_users_vector_urls(data_file, urls):
    users = {}
    user_id = -1
    user = [0 for i in range(dim)]
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if int(user_id) >= 0 and int(line[0]) != user_id:
                    users[user_id] = user
                    user = [0 for i in range(dim)]
            if(int(line[5]) == 2):
                url = urls[int(line[4])]
                if (int(line[3]) < n_trainig_days_):
                    #weight = int(line[3])/7 + 1)
                    weight = 1.
                    #weight = 1./math.sqrt(n_trainig_days_ - int(line[3]))
                    #if (random.randint(0,1) == 0):
                    user = [user[i] + weight * url[i] for i in range(dim)]
            user_id = int(line[0])

    return users

def Get_users_vector(data_file, queries):
    users = {}
    user_id = -1
    user = [0 for i in range(dim)]
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 == 0):
                if int(user_id) >= 0 and int(line[0]) != user_id:
                    users[user_id] = user
                    user = [0 for i in range(dim)]
                query = queries[line[2]]
                if (int(line[3]) < n_trainig_days_):
                    #weight = int(line[3])/7 + 1)
                    #weight = 1.
                    weight = 1./math.sqrt(n_trainig_days_ - int(line[3]))
                    #if (random.randint(0,1) == 0):
                    user = [user[i] + weight * query[i] for i in range(dim)]
                user_id = int(line[0])

    return users

def Get_users_neigbours(users, res_file):
    res = {}
    n_neigbours = 10
    j = 0
    for user in users.keys():
        print ("AAAA = " , j)
        j += 1
        res[user] = []
        d_users = [[Cos(users[user], users[other_user]), other_user] for other_user in users.keys()]
        d_users.sort(key = lambda x:-x[0])
        for i in range(n_neigbours):
            res[user].append(d_users[i][1])
        with open(res_file, 'w') as r_f:
            for u in res.keys():
                r_f.write(str(u) + "\t" + "\t".join(str(i) for i in res[u]) + "\n")
    return res

def Get_user_neigbours_from_file(user_file):
    res = {}
    with open(user_file) as users:
        for line in users:
            line = line.strip().split('\t')
            res[int(line[0])] = [int(i) for i in line[1:]]
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

def Get_result(data_file, users_vector, query_features, users_neighbours):
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
                user_clicks.append([line[4], int(line[5]), int(line[6])])
            else:
                if (day >= n_trainig_days_ and len(user_clicks) > 0):
                    users = users_neighbours[int(user_id)]
                    #users = set([q[1] for q in query_features[query_id]])
                    d_users = [[Cos(users_vector[int(user_id)], users_vector[int(u)]),u] for u in users if int(user_id) in users_vector and int(u) in users_vector]
                    d_users.sort(key = lambda x : -x[0])
                    n_users = min(10, len(d_users))
                    #user_vector = users_vector[int(user_id)]
                    click_predicion = {}
                    for u in user_clicks:
                        click_predicion[u[0]] = 0
                    user_clicks.sort(key = lambda x: x[2])
                    friends = [d_users[i][1] for i in range(n_users)]
                    urls = [i[0] for i in user_clicks]
                    friends_clicks = [[u[0], u[1], u[2]] for u in query_features[query_id] if int(u[1]) in friends and u[0] in urls]
                    for cl in friends_clicks:
                        d = Cos(users_vector[int(cl[1])], users_vector[int(user_id)])
                        if (d >= 0.5):
                            #weight = (n_trainig_days_-cl[2]) / n_trainig_days_
                            weight = 1./ math.sqrt(n_trainig_days_ - cl[2])
                            #weight = 1.
                            click_predicion[cl[0]] += d * weight
                    navigational, basic, prediction_done, actually_prediction_navigation = \
                        Get_prediction(click_predicion, user_clicks)
                    n_all_queries += 1
                    n_right_prediction_navigation += navigational
                    n_right_prediction_basic += basic
                    n_predictions += prediction_done
                    n_right_actually_prediction_navigation += actually_prediction_navigation

                user_clicks = [[line[4], int(line[5]), int(line[6])]]
                query_id = line[2]
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
        make_predictions = 1
    a = [i[1] for i in user_clicks if i[0] == prediction[0]]
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
    users_vector = Get_users_vector_urls(data_file, Get_queries_features(urls_name))
    queries_vector = Get_new_features_for_query(data_file, queries_name)
    #users_neighbours = Get_users_neigbours(users_vector, "../../data/users_neighbours")
    users_neighbours = Get_user_neigbours_from_file("../../data/users_neighbours")
    Get_result(data_file, users_vector, queries_vector, users_neighbours)

main()