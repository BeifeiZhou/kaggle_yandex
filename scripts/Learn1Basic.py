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
            if (int(line[3]) < n_validation_days and int(line[5]) == 2):
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

def Get_local_features(user_history, user_clicks, query, url, rank, urls_counts, query_counts):

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
    click_cout_to_url = urls_counts[url]
    query_count = query_counts[query]
    return [url_statistic[u] for u in urls] + [click_count_to_url_user, click_count_to_url_query, click_cout_to_url,
                                                                  query_count, query_count_user, different_queries]


def Get_result(data_file, learn_train_file, test_file, urls_counts, query_counts):
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
                        features = Get_local_features(user_history, user_clicks, query_id, url, rank, urls_counts, query_counts)
                        if (day >= n_training_days):
                            test.write("\t".join(str(i) for i in features) + "\t" + str(url_info[1]) + "\n")
                        else:
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
    data_file = "../../data/trainW2V"
    test_file = "../../data/testForIdea"
    validation_file = "../../data/validation"

    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    urls_counts = Get_clicks_for_urls(data_file, urls_name)
    query_counts = Get_queries_asked(data_file, queries_name)

    Get_result(data_file, validation_file, test_file, urls_counts, query_counts)

main()