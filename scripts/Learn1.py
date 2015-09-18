__author__ = 'annasepliaraskaia'

from get_items import *
from Create_features_as_summ_urls import *

n_validation_days = 22
n_training_days= 25

def Get_user_neighbours(neighbours_file):
    res = {}
    with open(neighbours_file) as neighbours:
        for line in neighbours:
            line = line.strip().split("\t")
            res[int(line[0])] = [int(u) for u in line[1:4]]
    return res

def Get_click_statistic_by_neighbours(url, users_neughbours,  urls_vector,
                                          users_vector, urls):
    click_statistic_by_n = []
    click_summ = {}
    for user_ in users_neughbours:
        for url_ in urls:
            click_statistic_by_n.append(Scalar_vectors(urls_vector[url_], users_vector[user_]))
        click_summ[user_] = (sum(click_statistic_by_n[-10:]))

    click_probability = []
    for user_ in users_neughbours:
        click_statistic_by_n.append(Scalar_vectors(urls_vector[url], users_vector[user_]) / (click_summ[user_] + 1e-10))
    return click_statistic_by_n

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

def Get_local_features(url, query, user, rank,  urls_vector, query_vector, users_vector, user_clicks, user_history,
                       users_neighbours):

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
    return [scalar_products_on_urls[u] for u in urls_in_query] + [click_count_to_url_user, click_count_to_url_query,
                                                                  click_cout_to_url,
                                                                  query_count, query_count_user,
                                                                  different_queries, rank] + \
                                                Get_click_statistic_by_neighbours(url, users_neighbours,  urls_vector,
                                                                                                  users_vector, urls_in_query)

def Get_result(data_file,
               urls_vector, query_features, users_vector,
               users_neighbours,
               validation_files,
               test_files):
    user_history = {}
    user_clicks = []
    query_id = -1
    user_id = -1
    day = -1
    user_position_baies = [0 for i in range(10)]

    with open(data_file) as data, \
            open(validation_files[0], 'w') as v_n,\
            open(validation_files[1], 'w') as v_s_s,\
            open(validation_files[2], 'w') as v_s,\
            open(test_files[0], 'w') as t_n,\
            open(test_files[1], 'w') as t_s_s,\
            open(test_files[2], 'w') as t_s\
            :
        for line_n, line in enumerate(data):
            if (line_n%10**4 == 0):
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
                                                query_features, users_vector, user_clicks, user_history,
                                                users_neighbours[user_id])


                        str_to_write = "\t".join(str(i) for i in features) \
                                       + "\t" + "\t".join(str(i) for i in user_position_baies) \
                                        +"\t" + str(url_info[1]) + "\n"
                        query_st = features[13]
                        if (day >= n_training_days):
                            if (query_st < 1):
                                t_n.write(str_to_write)
                            elif (query_st < 10):
                                t_s_s.write(str_to_write)
                            else:
                                t_s.write(str_to_write)
                        else:
                            if (max(u[1] for u in user_clicks) > 1):
                                if (query_st < 1):
                                    v_n.write(str_to_write)
                                elif (query_st < 10):
                                    v_s_s.write(str_to_write)
                                else:
                                    v_s.write(str_to_write)
                            #if (max(u[1] for u in user_clicks) > 1):
                            #    train.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")

                elif(len(user_clicks) > 0 and int(line[3]) >= n_validation_days - 21):
                    for cl in user_clicks:
                        if (cl[1] == 2):
                            user_position_baies[cl[2]] += 1
                            if (int(query_id) not in user_history):
                                user_history[int(query_id)] = {}
                            if (int(cl[0]) not in user_history[int(query_id)]):
                                user_history[int(query_id)][int(cl[0])] = 0
                            user_history[int(query_id)][int(cl[0])] += 1
                if (user_id != int(line[0])):
                    user_history = {}
                    user_position_baies = [0 for i in range(10)]

                user_clicks = [[int(line[4]), int(line[5]), int(line[6])]]
                query_id = int(line[2])
                user_id = int(line[0])
                day = int(line[3])

def main():
    directory = "../../my_data/"
    data_file = "../../data/trainW2V_small"

    validation_file_new =  directory + "validation_new"
    validation_with_some_statistic = directory + "validation_a_few_st"
    validation_with_stat = directory + "validation_st"
    validation_files = [validation_file_new, validation_with_some_statistic, validation_with_stat]

    test_file_new = directory + "test_new"
    test_with_some_statistic = directory + "test_a_few_st"
    test_with_stat = directory + "test_st"
    tests_file = [test_file_new, test_with_some_statistic, test_with_stat]


    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    users_features = Get_features(users_name)
    urls_vector = Get_url_features(data_file, users_features, urls_name)
    query_features = Get_queries_features(data_file, users_features, queries_name)

    users_neighbours = Get_user_neighbours("../../data/users_neighbours")

    Get_result(data_file,
               urls_vector, query_features, users_features,
               users_neighbours, validation_files, tests_file)

main()
