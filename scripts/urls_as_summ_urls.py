__author__ = 'annasepliaraskaia'
from get_items import *
from W2V import *
import numpy as np

n_validation_days = 22
n_training_days = 25
dim = 100


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


def get_features(queries_name, dim):
    res = {}
    for q in queries_name:
        res[q] = np.array(Get_random_vector(dim))
    return res


def cos(a, b):
    return np.inner(a, b) / (math.sqrt(np.inner(a,a) * np.inner(b, b)) + 1e-10)


def get_local_features(user_clicks, user, users_vector_as_queries, users_vector_as_urls,
                       urls_vector, rank, users_query, query):

    n_features = 11
    if query not in users_query:
        return [0 for i in range(n_features)] + [rank]
    d = [[u, cos(users_vector_as_queries[user], users_vector_as_queries[u])] for u in users_query[query]]
    d.sort(key=lambda x: -x[1])
    n_neighbours = min(30, len(d))

    features = [0 for i in range(10)]
    url_count = 0
    for u_n, u in enumerate(user_clicks):
        for n in range(n_neighbours):
            features[u_n] += np.inner(urls_vector[u[0]], users_vector_as_urls[d[n][0]])
    return features + [features[rank], rank]


def get_data(data_file, train_f, test_f,
                 users_vector_as_queries, users_vector_as_urls,
                 urls_vector, users_query):
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1

    with open(data_file) as data, open(train_f, 'w') as train, open(test_f, 'w') as test:
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
                        if (sum(np.inner(urls_vector[u[0]], users_vector_as_urls[user_id]) for u in user_clicks) < 0.05):
                            features = get_local_features(user_clicks, user_id, users_vector_as_queries, users_vector_as_urls,
                                urls_vector, rank, users_query, query_id)


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
    data_file = "../../big_data/trainW2V_small_q"
    test_f = "../../big_data/trainW2V_small_q_test"
    train_f = "../../big_data/trainW2V_small_q_validation"

    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    query_vector = get_features(queries_name, dim)
    users_vector_as_queries = users_as_sum_queries(data_file, query_vector, users_name)
    query_vector.clear()

    urls_vector = get_features(urls_name, dim)
    users_vector_as_urls = users_as_sum_urls(data_file, urls_vector, users_name)

    users_query = users_that_entered_query(data_file, queries_name)

    get_data(data_file, train_f, test_f,
                 users_vector_as_queries, users_vector_as_urls,
                 urls_vector, users_query)

def get_queries():
    res = []
    with open("../../big_data/queries") as q:
        for line in q:
            res.append(int(line.strip()))
    res = set(res)
    with open("../../big_data/trainW2V_small") as t, open("../../big_data/trainW2V_small_q", 'w') as r:
        for line in t:
            line1 = line.strip().split("\t")
            if (int(line1[2]) in res):
                r.write(line)
#main1()





