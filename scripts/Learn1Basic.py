__author__ = 'annasepliaraskaia'

from get_items import *

n_validation_days = 22
n_training_days= 25

def Get_clicks_for_urls(data_file, urls_name):
    print("Get users features")
    res = {}
    for u in urls_name:
        res[u] = 0
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (int(line[3]) < n_validation_days and int(line[5]) >= 0):
                res[int(line[4])] += 1
    return res

def Get_clicks_for_urls_first_time_quiry(data_file, query_name):
    print("Get users features")
    res = {}
    for q in query_name:
        res[q] = {}
    user_id = -1
    user_clicks = {}
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (user_id != int(line[0])):
                user_clicks = {}
            user_id = int(line[0])
            if (int(line[3]) < n_validation_days and int(line[5]) >= 2):
                if (int(line[2]) not in user_clicks):
                    user_clicks[int(line[2])] = 1
                    if (int(line[2]) not in res):
                        res[int(line[2])] = {}
                    if (int(line[4]) not in res[int(line[2])]):
                        res[int(line[2])][int(line[4])] = 0
                    res[int(line[2])][int(line[4])] += 1
    return res

def Get_clicks_for_urls_first_time(data_file, urls_name):
    print("Get users features")
    res = {}
    for u in urls_name:
        res[u] = 0
    user_id = -1
    user_clicks = {}
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (user_id != int(line[0])):
                user_clicks = {}
            user_id = int(line[0])
            if (int(line[3]) < n_validation_days and int(line[5]) >= 2):
                if (int(line[2]) not in user_clicks):
                    user_clicks[int(line[2])] = 1
                    res[int(line[4])] += 1
    return res

def Get_queries_asked(data_file, query_name):
    print("Get queries features")
    res = {}
    for q in query_name:
        res[q] = 0
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (int(line[3]) < n_validation_days and line_n%10 == 0):
                res[int(line[2])] += 1
    return res

def Get_urls_statistic(urls, user_history):
    url_statistic = {}
    for u in urls:
        url_statistic[u] = 0
    for q in user_history.keys():
        for u in urls:
            if(u in user_history[q]):
                url_statistic[u] += user_history[q][u]
    return url_statistic

def Get_local_features(user_history, user_clicks, query, url, rank, urls_counts,
                       urls_count_first_time_query, urls_count_first_time,
                       query_counts):

    urls = [u[0] for u in user_clicks]
    url_statistic = Get_urls_statistic(urls, user_history)
    click_count_to_url_user = url_statistic[url]
    click_count_to_url_query = 0.
    if (query in user_history and url in user_history[query]):
        click_count_to_url_query = user_history[query][url]
    query_count_user = 0
    if (query in user_history):
        query_count_user = user_history[query][-1]
    different_queries = len(user_history.keys())
    #click_cout_to_url = urls_count_first_time[url]
    query_count = query_counts[query]



    click_count_to_urls_query = [0 for u in urls]
    click_count_url_query = 0
    if (int(query) in urls_count_first_time_query):
        for u_n, u in enumerate(urls):
            if (int(u) in urls_count_first_time_query[query]):
                click_count_to_urls_query[u_n] = urls_count_first_time_query[query][u]
                if (u == url):
                    click_count_url_query = urls_count_first_time_query[query][u]

    click_count_url = 0
    sum_click_count = 0
    for u in urls:
        sum_click_count += urls_count_first_time[u]
        if (u == url):
            click_count_url = urls_count_first_time[u]
    #click_cout_to_urls = [urls_count_first_time[u] for u in urls]
    return [float(click_count_url_query) / (sum(click_count_to_urls_query) + 1e-10),
            float(click_count_url) / (sum_click_count + 1e-10), sum_click_count, rank ]


def Get_result(data_file, learn_train_file, test_file, urls_counts,
               urls_count_first_time_query, urls_count_first_time,
               query_counts):
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
                    for rank, url_info in enumerate(user_clicks):
                        url = url_info[0]
                        features = Get_local_features(user_history, user_clicks, query_id, url, rank, urls_counts,

                                                    urls_count_first_time_query, urls_count_first_time,
                                                    query_counts)

                        if (day >= n_training_days):
                            #if (max(abs(cl) for cl in features[:10]) == 0 and sum(cl for cl in features[12:22]) > 100):
                            test.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")
                        else:
                            if (max(u[1] for u in user_clicks) > 1):
                                #if (max(abs(cl) for cl in features[:10]) == 0 and sum(cl for cl in features[12:22]) > 100):
                                 train.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")

                elif(len(user_clicks) > 0 and int(line[3]) >= n_validation_days - 21):
                    for cl in user_clicks:
                        if (cl[1] == 2):
                            if (int(query_id) not in user_history):
                                user_history[int(query_id)] = {}
                                user_history[int(query_id)][-1] = 0
                            user_history[int(query_id)][-1] += 1
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
    data_file = "../../big_data/trainW2V_medium"
    test_file = "../../data/testForIdea"
    validation_file = "../../data/validation"

    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    urls_counts = Get_clicks_for_urls(data_file, urls_name)
    urls_count_first_time_query = Get_clicks_for_urls_first_time_quiry(data_file, queries_name)
    urls_count_first_time = Get_clicks_for_urls_first_time(data_file, urls_name)

    query_counts = Get_queries_asked(data_file, queries_name)

    Get_result(data_file, validation_file, test_file, urls_counts,
               urls_count_first_time_query, urls_count_first_time,
               query_counts)

main()
