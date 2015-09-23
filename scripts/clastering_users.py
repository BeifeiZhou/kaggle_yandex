__author__ = 'annasepliaraskaia'
import random
from get_items import *

n_validation_days = 22

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

class Clustering(object):
    def __init__(self, n_clusters, users_name, query_names, data_file):
        self.n_clusters = n_clusters
        self.data_file = data_file
        self.users = {}
        for u in users_name:
            self.users[u] = [0. for i in range(n_clusters)]
            self.users[u][random.randint(0, n_clusters-1)] = 1.
        self.query = {}
        n_documents_in_serp = 10
        for q in query_names:
            self.query[q] = {}
            for i in range(n_clusters):
                self.query[q][i] = {}


    def Get_data(self, new_queries, change_queries,
                 user_stat, user_new):
        user_history = {}
        user_clicks = []
        query_id = -1
        user_id = -1
        day = -1

        with open(self.data_file) as data:
            for line_n, line in enumerate(data):
                if (line_n%10**6 == 0):
                    print(line_n)
                line = line.strip().split("\t")
                if (line_n%10 != 0):
                    user_clicks.append([int(line[4]), int(line[5]), int(line[6])])
                else:
                    if(len(user_clicks) > 0 and int(day) < n_validation_days):
                        user_clicks.sort(key = lambda x: x[2])
                        if (int(query_id) not in user_history and not change_queries):
                            self.One_step_one_user_change_user(query_id, user_id, user_clicks,
                                                               user_stat, user_new)
                        for cl in user_clicks:
                            if (cl[1] == 2):
                                if (int(query_id) not in user_history):
                                    user_history[int(query_id)] = {}
                                    if (int(cl[0]) not in user_history[int(query_id)]):
                                        user_history[int(query_id)][int(cl[0])] = 1

                    if (user_id != int(line[0]) and len(user_clicks) > 0):
                        if (change_queries):
                            self.One_step_one_user_change_query(user_id, user_history, new_queries)
                        user_history = {}

                    user_clicks = [[int(line[4]), int(line[5]), int(line[6])]]
                    query_id = int(line[2])
                    user_id = int(line[0])
                    day = int(line[3])

    def One_step_one_user_change_query(self, user, user_history, new_queries):
        for cluster_n, cluster_prob in enumerate(self.users[user]):
            if (cluster_prob > 0):
                for q in user_history.keys():
                    for url in user_history[q].keys():
                        if (url not in new_queries[q][cluster_n]):
                            new_queries[q][cluster_n][url] = 0
                        new_queries[q][cluster_n][url] += cluster_prob

    def One_step_change_query(self):
        new_queries = {}
        for q in self.query.keys():
             new_queries[q] = {}
             for i in range(self.n_clusters):
                 new_queries[q][i] = {}

        user_stat = {}
        user_new = {}
        self.Get_data(new_queries, True,
                 user_stat, user_new)
        self.query = new_queries

    def Get_result_from_query_one_cluster(self, cluster, query, urls):
        res = 0
        max_count = 0
        for u_n,u in enumerate(urls):
            if (u in self.query[query][cluster]):
                if (max_count < self.query[query][cluster][u]):
                    max_count = self.query[query][cluster][u]
                    res = u_n

        return res

    def One_step_one_user_change_user(self, query, user, user_clicks, user_stat, user_new):
        for cluster in range(self.n_clusters):
            urls = [u[0] for u in user_clicks]
            prediction = self.Get_result_from_query_one_cluster(cluster, query, urls)
            truth = max(u[1] for u in user_clicks)
            if (user_clicks[prediction][1] == truth):
                user_new[user][cluster] += 1
                user_stat[user] += 1

    def One_step_change_users(self):

        user_new = {}
        user_stat = {}
        for u in self.users:
            user_stat[u] = 0
            user_new[u] = [0. for i in range(self.n_clusters)]
        new_queries = {}
        self.Get_data(new_queries, False,
                 user_stat, user_new)
        for u in user_new.keys():
            for cluster in range(self.n_clusters):
                user_new[u][cluster] = float(user_new[u][cluster] / (user_stat[u]  +1e-10))
            if (sum(user_new[u]) < 1e-10):
                for cluster in range(self.n_clusters):
                    user_new[u][cluster] = 1./self.n_clusters
        self.users = user_new

    def Get_result(self, user, query, urls):
        result = [0 for i in range(len(urls))]
        for u_n,u in enumerate(urls):
            for cluster_number, cluster_prob in enumerate(self.users[user]):
                if u in self.query[query][cluster_number]:
                    result[u_n] += cluster_prob * self.query[query][cluster_number][u]
        return result


def main():
    data_file = "../../big_data/trainW2V_small_small"

    queries_name = Get_queries(data_file)
    urls_name = Get_urls(data_file)
    users_name = Get_users(data_file)

    trainer = Clustering(10, users_name, queries_name, data_file)
    trainer.One_step_change_query()
    trainer.One_step_change_users()
    trainer.One_step_change_query()
    trainer.One_step_change_users()

#main()

