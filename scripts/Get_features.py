__author__ = 'annasepliaraskaia'
import sys
import math
from W2V import *
#from linear_regression_and_hash_features import HashFeatures

class url(object):
    def __init__(self):
        self.url = -1
        self.domain = -1
        self.type = -2
        self.rank = -1

class serp(object):
    def __init__(self):
        self.session_id = -1
        self.serpId = -1
        self.QueryId = -1
        self.time_passed = -1
        self.listOfTerms = []
        self.listOfUrlsAndDomains = {} # dictionary of url
        self.last_clicked_rank = -1
        self.people_id = -1
        self.day = -1

class basic_features(object):
    def __init__(self):
        feature = {}
        terms = ["termId1","termId2", "termId3"]
        feature["position"] = -1
        feature["queryId"] = -1
        feature["urlID"] = -1
        feature["domainId"] = -1
        feature["urlId_queryId"] = -1
        feature["domainId_Position"] = -1
        for term in terms:
            feature[term] = -1
            feature["urlId_" + term] = -1
            feature["domainI_" + term] = -1
        self.features = feature


def Click_types(time):
    if (time < 50):
       return 0
    if (time < 300):
          return 1
    return 2

class Working_with_data(object):

    def Get_ListOfURLsAndDomains(self, lUD):
        urls = {}
        i = 0
        for UD in lUD:
            UD = UD.split(',')
            url_info = url()
            url_info.domain = float(UD[1])
            url_info.rank = i

            urls[UD[0]] = url_info
            i += 1
        return urls

    def Get_list_of_terms(self,list_of_terms):
        return list_of_terms.split(',')

    def Get_data_with_type_of_record_Q(self,line):
        res_serp = serp()
        res_serp.time_passed = float(line[1])
        #res_serp.typeOfRecord = line[2]
        res_serp.serpId = line[3]
        res_serp.QueryId = line[4]
        res_serp.listOfTerms = self.Get_list_of_terms(line[5])
        res_serp.listOfUrlsAndDomains = self.Get_ListOfURLsAndDomains(line[6:])
        return res_serp

    def Get_data_with_type_of_record_C(self,line):
        res = {}
        res['time_passed'] = float(line[1])
        res['serpId'] = line[3]
        res['urlId'] = line[4]
        return res

    def Get_data_with_type_of_record_M(self, line):
        res = {}
        res['day'] = int(line[2])
        res['userId'] = line[3]
        return res

    def Get_truth_for_one_serp(self, serp, clicks):
        n_clicks = len(clicks)
        if (n_clicks == 0):
            return
        rang_last_click = -1
        serp.listOfUrlsAndDomains[clicks[n_clicks - 1]['urlId']].type = 2
        rang_last_click = serp.listOfUrlsAndDomains[clicks[n_clicks - 1]['urlId']].rank
        time = clicks[n_clicks-1]['time_passed']
        i = n_clicks-2
        while i >= 0:
            new_time = clicks[i]['time_passed']
            url_id = clicks[i]['urlId']
            serp.listOfUrlsAndDomains[url_id].type = Click_types(time-new_time)
            rang_last_click = max(rang_last_click, serp.listOfUrlsAndDomains[url_id].rank)
            i -= 1
        for key in serp.listOfUrlsAndDomains.keys():
            if (serp.listOfUrlsAndDomains[key].rank < rang_last_click):
                serp.listOfUrlsAndDomains[key].type = max(serp.listOfUrlsAndDomains[key].type, -1)
        serp.last_clicked_rank = rang_last_click

    def Get_basic_features(self, one_serp, file):
        terms = one_serp.listOfTerms
        terms.sort()
        while len(terms) < 3:
            terms.append("NULL")
        for url in one_serp.listOfUrlsAndDomains.keys():
            features = []
            feature_names = []
            url_info = one_serp.listOfUrlsAndDomains[url]

            features.append(url)
            feature_names.append("urlID")

            features.append(url_info.domain)
            feature_names.append("domainId")

            features.append(url_info.rank)
            feature_names.append("position")

            features.append(one_serp.QueryId)
            feature_names.append("queryId")

            features.append(str(url) + "," + str(one_serp.QueryId))
            feature_names.append("urlId_queryId")

            features.append(str(url_info.domain) + "," + str(url_info.rank))
            feature_names.append("domainId_Position")

            terms_name = ["termId1","termId2", "termId3"]
            for t_n, term in enumerate(terms_name):
                features.append(terms[t_n])
                feature_names.append(term)
                features.append(str(url)+","+terms[t_n])
                feature_names.append("urlId_" + term)
                features.append(str(url_info.domain)+","+terms[t_n])
                feature_names.append("domainId_" + term)

            f = HashFeatures(features, feature_names, 2**30)
            f.sort()
            file.write(str(one_serp.session_id)+ "," + str(url) + "\t".join(str(i) for i in f) + "\t" + str(url_info.type)
                       +"\n")

    def Write_features_for_W2V_format(self, one_serp, file):
        features_name = ["userId", "sessionId", "queryId", "day", "url", "urlType", "urlRang"]
        for url in one_serp.listOfUrlsAndDomains.keys():
            features = []
            url_info = one_serp.listOfUrlsAndDomains[url]
            features.append(one_serp.people_id)
            features.append(one_serp.session_id)
            features.append(one_serp.QueryId)
            features.append(one_serp.day)
            features.append(url)
            features.append(url_info.type)
            features.append(url_info.rank)
            file.write("\t".join(str(f) for f in features) + "\n")

    def Get_data(self,data_file):
        #assume that first M,then Q,then C
        n_users = 0
        clicks = {}
        serps = {}

        with open(data_file) as data:
            for i,line in enumerate(data):
                if (i%10**6 == 0):
                    print(i)
                if (n_users > 10**5):
                    break
                line = line.strip().split('\t')
                session_id = line[0]
                if (len(line) == 4):
                    if (len(clicks.keys()) > 0):
                        n_users += 1
                        for serp_id in serps.keys():
                            one_serp = serps[serp_id]
                            if (serp_id in clicks and len(clicks[serp_id]) > 0):
                                self.Get_truth_for_one_serp(one_serp, clicks[serp_id])
                                self.Write_features_for_W2V_format(one_serp, self.train_data)
                            #    if (one_serp.day > 24):
                            #        self.Get_basic_features(one_serp, self.test_data)
                            #    else:
                            #        self.Get_basic_features(one_serp, self.train_data)
                    clicks = {}
                    serps = {}
                    res = self.Get_data_with_type_of_record_M(line)
                    one_session = res

                elif (len(line) == 5):
                    res = self.Get_data_with_type_of_record_C(line)
                    if res["serpId"] not in clicks.keys():
                        clicks[res["serpId"]] = []
                    clicks[res["serpId"]].append(res)
                else:
                    res = self.Get_data_with_type_of_record_Q(line)
                    res.people_id = one_session['userId']
                    res.day = one_session['day']
                    res.session_id = session_id
                    if (line[2] == 'T'):
                        self.test_data.write(str(session_id) + "_" + str(res.serpId) + "\t")
                        self.Get_basic_features(res, self.test_data)
                    serps[res.serpId] = res


    def __init__(self,data_file,test_data_file, train_data_file):
        #self.test_data = open(test_data_file,'w')
        self.train_data = open(train_data_file, 'w')
        self.Get_data(data_file)

def Get_users_for_queries(data_file, res_file):
    queries = {}
    user_id = 0
    query = 0
    user_clicks = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (not line_n%10 == 0):
                user_clicks.append([int(line[-2]), int(line[-1])])
            if (line_n%10 == 0 and int(line[3]) < 24 and len(user_clicks) > 0):
                user_clicks.sort(key=lambda x: x[1])
                if (not user_clicks[0][0] == max([user_clicks[i][0] for i in range(len(user_clicks))])):
                    if (query not in queries):
                        queries[query] = []#Get_random_vector(100)
                    queries[query].append(user_id)
                user_id = line[0]
                query = line[2]
                user_clicks = [[int(line[-2]), int(line[-1])]]
    with open(res_file, 'w') as res:
        for q in queries.keys():
            if (len(queries[q]) > 1):
                res.write(str(q) + "\t" + "\t".join(str(u) for u in queries[q]) + "\n")
    return queries

def Get_user_features(data_file, res):
    dim = 100
    n_train_days = 25
    queries = Get_users_for_queries(data_file)
    users = {}
    users_urls = {}
    res_open = open(res, 'w')
    with open(data_file) as data:
        for line_n,line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            #for training set
            line = line.strip().split('\t')
            session_day = int(line[3])
            if (session_day < n_train_days):
                if line[0] not in users_urls:
                    users_urls[line[0]] = {}
                if line[4] not in users_urls[line[0]]:
                    users_urls[line[0]][line[4]] = [0 for i in range(5)]
                users_urls[line[0]][line[4]][int(line[5]) + 2] += 1
            if (line_n%10 == 0):
                if session_day < n_train_days:
                    if line[0] not in users:
                        users[line[0]] = [0 for i in range(dim)]
                    if (len(queries[line[2]]) > 100):
                        for i in range(dim):
                            users[line[0]][i] += (1./(n_train_days - session_day)) * queries[line[2]][i]

    with open(data_file) as data:
         ex = []
         truth = []
         basic_ndcg = 0
         basic_ex = []
         ndcg = 0
         n_ex = 0
         for line_n,line in enumerate(data):
             if (line_n%10 == 0):
                 if (len(ex) > 0):
                     person_ndcg = Get_ndcg_for_one_ex(ex, truth)
                     ndcg += Get_ndcg_for_one_ex(ex, truth)
                     ex_ = [[ex[i],truth[i]] for i in range(len(ex))]
                     ex_.sort(key=lambda x:(-x[0][-1]))


                     n_ex += 1
                     truth.sort(key = lambda x:-x)
                     print(truth)
                     basic_ndcg_one = DCG(basic_ex) / (DCG([[t, t] for t in truth]) + 1e-10)
                     basic_ndcg += DCG(basic_ex) / (DCG([[t, t] for t in truth]) + 1e-10)
                     if (person_ndcg != basic_ndcg_one):
                          res_open.write("\t".join(str(t[1]) for t in ex_) + "\t" +str(person_ndcg) + "\n")
                          res_open.write("\t".join(str(i[1]) for i in basic_ex) + "\t" + str(basic_ndcg_one) + "\n\n")

                 ex = []
                 basic_ex = []
                 truth = []
         # for test set
             line = line.strip().split('\t')
             if (line_n%10**6 == 0):
                 print(line_n)
             session_day = int(line[3])
             if (session_day >= n_train_days):
                 url = line[4]
                 user = line[0]
                 #print("user = ", user)
                 if line[2] in queries and user in users:
                     people = queries[line[2]][100:]
                     res_types = [0 for i in range(5)]
                     n_people = 0
                     for p in people:

                         d = Scalar_vectors(users[p],users[user])
                         d /= math.sqrt(Scalar_vectors(users[p], users[p]))
                         d /= math.sqrt(Scalar_vectors(users[user], users[user]))
                         for i in range(5):
                             if url in users_urls[p]:
                                 res_types[i] += users_urls[p][url][i]*d
                                 n_people += users_urls[p][url][i]*d
                     #res_open.write(user + "\t" + line[1] + "\t" + "\t".join(str(res_types[i]/(n_people+1e-10))
                     #                                                        for i in range(5)) + "\t" + line[5] + "\t" + line[6] + "\n")
                     ex.append(res_types)
                     tr = int(line[5])
                     if (tr <= 0):
                         tr = 0
                     truth.append(tr)
                     basic_ex.append([10-line_n%10,  tr])
         print (ndcg / n_ex)
         print (basic_ndcg / n_ex)


def Ex_score(ex):
    sum = 0
    positive = 0
    for i,e in enumerate(ex):
        sum += e*(i+1)
    return ex[-1]

def DCG(ex):
    res = 0
    for i in range(len(ex)):
        res += (2**ex[i][1] - 1)/math.log(i+2,2)
    return res

def Get_ndcg_for_one_ex(ex, truth):
    a = []
    b = []
    for i,e in enumerate(ex):
        a.append([Ex_score(ex[i]) + (10-i)/10., truth[i]])
        b.append([truth[i], truth[i]])
    a.sort(key = lambda x:-x[0])
    b.sort(key = lambda x:-x[0])
    if (DCG(a) > DCG(b)):
        print(DCG(a), DCG(b))
    return DCG(a) / (DCG(b)+1e-10)





#data = Working_with_data("../../data/train", "../../data/testW2V", "../../data/trainW2V")
Get_users_for_queries('../../data/trainW2V', '../../data/QueryUsers')
#Get_user_features("../../data/trainW2V", "../../data/users_for_queriesW2V")
