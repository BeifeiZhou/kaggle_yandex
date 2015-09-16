__author__ = 'annasepliaraskaia'

from get_items import *
from Create_features_as_summ_urls import *

n_validation_days = 22
n_training_days= 25

def Get_local_features(url, query, user, rank,  urls_vector, query_vector, users_vector, user_clicks, user_history):

    urls_in_query = [u[0] for u in user_clicks]
    scalar_products_on_urls = {}

    for url_ in urls_in_query:
        scalar_products_on_urls[url_] = Scalar_vectors(urls_vector[url_], users_vector[user])

    click_count_to_url_user = Scalar_vectors(urls_vector[url], users_vector[user])
    query_count_user = Scalar_vectors(query_vector[query], users_vector[user])
    click_count_to_url_query = query_count_user * (scalar_products_on_urls[url] /
                                                          (sum(scalar_products_on_urls[k] for k in urls_in_query) + 1e-10))
    click_cout_to_url = Scalar_vectors(urls_vector[url], urls_vector[url])
    query_count = Scalar_vectors(query_vector[query], query_vector[query])

    different_queries = len(user_history.keys())
    return [scalar_products_on_urls[u] for u in urls_in_query] + [click_count_to_url_user, click_count_to_url_query, click_cout_to_url,
                                                                  query_count, query_count_user, different_queries, rank]

def Get_result(data_file, learn_train_file, test_file,
               urls_vector, query_features, users_vector):
    user_history = {}
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1

    with open(data_file) as data, open(learn_train_file, 'w') as train, open(test_file, 'w') as test:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 != 0):
                user_clicks.append([int(line[4]), int(line[5]), int(line[6])])
            else:
                if (day >= n_validation_days and len(user_clicks) > 0):
                    user_clicks.sort(key = lambda x: x[2])
                    for rank,url_info in enumerate(user_clicks):
                        url = url_info[0]
                        features = Get_local_features(url, query_id, user_id, rank, urls_vector,
                                                query_features, users_vector, user_clicks, user_history)
                        if (day >= n_training_days):
                            test.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")
                        else:
                            train.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")

                elif(len(user_clicks) > 0 and int(line[3]) >= n_validation_days - 21):
                    for cl in user_clicks:
                        if (cl[1] == 2):
                            if (int(query_id) not in user_history):
                                user_history[int(query_id)] = {}
                            if (int(cl[0]) not in user_history[int(query_id)]):
                                user_history[int(query_id)][int(cl[0])] = 0
                            user_history[int(query_id)][int(cl[0])] += 1
                if (user_id != int(line[0])):
                    user_history = {}

                user_clicks = [[int(line[4]), int(line[5]), int(line[6])]]
                query_id = int(line[2])
                user_id = int(line[0])
                day = int(line[3])

def main():
    data_file = "../../data/trainW2V"
    test_file = "../../data/testForIdea"
    validation_file = "../../data/validation"

    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    users_features = Get_features(users_name)
    urls_vector = Get_url_features(data_file, users_features, urls_name)
    query_features = Get_queries_features(data_file, users_features, queries_name)

    Get_result(data_file, validation_file, test_file,
               urls_vector, query_features, users_features)

main()
