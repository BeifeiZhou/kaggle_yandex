import sys
import json

class Working_with_data(object):

    def Get_ListOfURLsAndDomains(self, lUD):
        urls_info = {}
        i = 0
        for UD in lUD:
            UD = UD.split(',')
            url_info = {}
            url_info['domain'] = UD[1]
            url_info['rank'] = i
            url_info['time_passed'] = {}
            urls_info[UD[0]] = url_info
            i += 1
        return urls_info

    def Get_list_of_terms(self,list_of_terms):
        return list_of_terms.split(',')

    def Get_data_with_type_of_record_Q(self,line):
        res = {}
        res['time_passed'] = float(line[1])
        res['typeOfRecord'] = line[2]
        res['serpId'] = line[3]
        res['QueryId'] = line[4]
        res['listOfTerms'] = self.Get_list_of_terms(line[5])
        res['listOfUrlsAndDomains'] = self.Get_ListOfURLsAndDomains(line[6:])
        return res

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

    def Get_data(self,data_file):
        #assume that first M,then Q,then C
        #self.data_by_sessions = {}
        one_session = {}
        self.people = {}
        with open(data_file) as data,open('../my_data/train', 'w') as result:
            for i,line in enumerate(data):
                #if (i > 10**6):
                #    break
                if (i%10**6 == 0):
                    print(i)
                line = line.strip().split('\t')
                session_id = line[0]

                #if session_id not in self.data_by_sessions and len(self.data_by_sessions.keys()) > 0 and len(line) != 4:
                #    continue
                if (len(line) == 4):
                    if (len(one_session.keys()) > 0):
                        result.write(json.dumps(one_session) + '\n')
                    one_session = {}
                    res = self.Get_data_with_type_of_record_M(line)

                    #if (len(self.people.keys()) > 10 and res['userId'] not in self.people):
                    #    continue
                    #if (res['userId'] not in self.people):
                    #    self.people[res['userId']] = [session_id]
                    #else:
                    #    self.people[res['userId']].append(session_id)

                    one_session = res


                elif (len(line) == 5):
                    res = self.Get_data_with_type_of_record_C(line)
                    one_session[res['serpId']]['listOfUrlsAndDomains'][res['urlId']]['time_passed'] = (
                        res['time_passed'])
                else:
                    res = self.Get_data_with_type_of_record_Q(line)
                    one_session[res['serpId']] = res

    def __init__(self,data_file):
        self.Get_data(data_file)

def main():
    data = Working_with_data(sys.argv[1])
    #for i,people in data.people:
    #    with open('../my_data/user_' + str(i), 'w') as user:
    #        for session in people:
    #            user.write(data.data_by_sessions[session] + '\n\n\n')
main()