__author__ = 'annasepliaraskaia'
from get_items import *
from W2V import *
import numpy as np

n_validation_days = 22
n_training_days = 25
dim = 40


def users_as_sum_queries(data_file, queries_vector, users_name):
    result = {}
    for u in users_name:
        result[u] = np.zeros(dim)

    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if line_n % 10**6 == 0:
                print(line_n)
            if line_n%10 == 0:
                line = line.strip().split("\t")
                if int(line[3]) < n_validation_days:
                    result[int(line[0])] += queries_vector[int(line[2])]
    return result


def users_as_sum_urls(data_file, urls_vector, users_name):
    result = {}
    for u in users_name:
        result[u] = np.zeros(dim)

    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if line_n%10**6 == 0:
                print(line_n)
            line = line.strip().split("\t")
            if int(line[5]) >= 2 and int(line[3]) < n_validation_days:
                result[int(line[0])] += urls_vector[int(line[4])]
    return result


def users_that_entered_query(data_file, query_names):
    res = {}
    for q in query_names:
        res[q] = []

    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if line_n%10**6 == 0:
                print(line_n)
            if line_n % 10 == 0:
                line = line.strip().split("\t")
                if int(line[3]) < n_validation_days:
                    res[int(line[2])].append(int(line[0]))
    for q in query_names:
        res[q] = set(res[q])
    return res


def query_emmissed_by_user(data_file, users_names):
    res = {}
    for u in users_names:
        res[u] = []

    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if line_n%10**6 == 0:
                print(line_n)
            if line_n % 10 == 0:
                line = line.strip().split("\t")
                if int(line[3]) < n_validation_days:
                    res[int(line[0])].append(int(line[2]))
    for u in users_names:
        res[u] = set(res[u])
    return res


def cliked_document_by_user(data_file, users_names):

    res = {}
    for u in users_names:
        res[u] = []

    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if line_n%10**6 == 0:
                print(line_n)
            line = line.strip().split("\t")
            if int(line[3]) < n_validation_days and int(line[5]) >= 2:
                    res[int(line[0])].append(int(line[4]))
    for u in users_names:
        res[u] = set(res[u])
    return res


def cos(a, b):
    return np.inner(a, b) / (math.sqrt(np.inner(a,a) * np.inner(b, b)) + 1e-10)


def set_similairity(a, b):
    res = float(len(a.intersection(b))) / len(a.union(b))
    return res

def get_local_features(user_clicks, user, clicked_urls,
                       rank, users_query, emmised_queries, query,  users_file):

    n_features = 11
    if query not in users_query:
        return [0 for i in range(n_features)] + [rank]
    #d = [[u, cos(users_vector_as_queries[user], users_vector_as_queries[u])] for u in users_query[query]
    #     if min(users_norm[u], users_norm[user]) / (max(users_norm[u], users_norm[user]) + 1e-10)]
    d = [[u, set_similairity(clicked_urls[user], clicked_urls[u])] for u in users_query[query] if
              len(clicked_urls[user].intersection(clicked_urls[u])) > 0]

    d.sort(key=lambda x: -x[1])
    n_neighbours = min(100, len(d))

    features = [0 for i in range(10)]
    url_count = 0
    to_write = str(user) + "\t" + "\t".join(str(i[0]) + "\t" + str(i[1]) for i in d[0:n_neighbours-1]) + "\n"
    users_file.write(to_write)
    for u_n, u in enumerate(user_clicks):
        for n in range(n_neighbours):
            if u[0] in clicked_urls[d[n][0]]:
                features[u_n] += 1
    return features + [features[rank], rank]


def get_data(data_file, train_f, test_f, clicked_urls,
                 users_query, emmised_queries):
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1

    with open(data_file) as data, open(train_f, 'w') as train, open(test_f, 'w') as test, \
        open("../../big_data/users1", 'w') as users:
        for line_n, line in enumerate(data):
            if (line_n%10**4 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 != 0):
                user_clicks.append([int(line[4]), int(line[5]), int(line[6])])
            else:
                if (day >= n_validation_days and len(user_clicks) > 0):
                    user_clicks.sort(key = lambda x: x[2])
                    for rank, url_info in enumerate(user_clicks):
                        url = url_info[0]
                        features = []
                        if (len(clicked_urls[user_id].intersection(set(u[0] for u in user_clicks))) == 0):
                            features = get_local_features(user_clicks, user_id, clicked_urls,
                       rank, users_query, emmised_queries, query_id,  users)


                        if (day >= n_training_days and len(features) > 0):
                            test.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")
                        else:
                            if max(u[1] for u in user_clicks) > 1 and len(features) > 0:
                                train.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")


                user_clicks = [[int(line[4]), int(line[5]), int(line[6])]]
                query_id = int(line[2])
                user_id = int(line[0])
                day = int(line[3])

def main1():
    data_file = "../../big_data/trainW2V"
    test_f = "../../big_data/trainW2V_small_test_q"
    train_f = "../../big_data/trainW2V_small_validation_q"

    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    #query_vector = get_features(queries_name, dim)
    #users_vector_as_queries = users_as_sum_queries(data_file, query_vector, users_name)
    #query_vector.clear()

    #urls_vector = get_features(urls_name, dim)
    #users_vector_as_urls = users_as_sum_urls(data_file, urls_vector, users_name)

    users_query = users_that_entered_query(data_file, queries_name)
    emmised_queries = query_emmissed_by_user(data_file, users_name)
    clicked_urls = cliked_document_by_user(data_file, users_name)
    #users_norm = {}
    #i  = 0
    #for key in users_vector_as_queries.keys():
    #    if (i % 1000 == 0):
    #        print i
    #    i += 1
    #    users_norm[key] = np.inner(users_vector_as_queries[key], users_vector_as_queries[key])

    get_data(data_file, train_f, test_f, clicked_urls,
                 users_query, emmised_queries)

def get_queries():
    res = []
    with open("../../big_data/queries") as q:
        for line in q:
            res.append(int(line.strip()))
    res = set(res)
    with open("../../big_data/trainW2V") as t, open("../../big_data/trainW2V_small_q", 'w') as r:
        for line in t:
            line1 = line.strip().split("\t")
            if (int(line1[2]) in res):
                r.write(line)
#main1()





