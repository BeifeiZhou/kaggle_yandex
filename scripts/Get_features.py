__author__ = 'annasepliaraskaia'
import sys
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
            file.write(str(one_serp.session_id)+ "," + str(url) + "\t".join(str(i) for i in f) + "\t" + str(url_info.type) +"\n")

    def Get_data(self,data_file):
        #assume that first M,then Q,then C

        clicks = {}
        serps = {}

        with open(data_file) as data:
            for i,line in enumerate(data):
                if (i%10**6 == 0):
                    print(i)
                line = line.strip().split('\t')
                session_id = line[0]
                if (len(line) == 4):
                    if (len(clicks.keys()) > 0):
                        for serp_id in serps.keys():
                            one_serp = serps[serp_id]
                            #if (serp_id in clicks and len(clicks[serp_id]) > 0):
                            #    self.Get_truth_for_one_serp(one_serp, clicks[serp_id])
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
        self.test_data = open(test_data_file,'w')
        self.train_data = open(train_data_file, 'w')
        self.Get_data(data_file)

#data = Working_with_data("../../data/test", "../../data/real_test", "../../data/real_test1")