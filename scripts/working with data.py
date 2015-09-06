import sys
import json
import struct
from session import session

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
        with open(data_file) as data,open('../my_data/train', 'w') as result:
            for i,line in enumerate(data):
                if (i%10**6 == 0):
                    print(i)
                line = line.strip().split('\t')
                session_id = line[0]
                if (len(line) == 4):
                    if (len(one_session.keys()) > 0):
                        result.write(json.dumps(one_session) + '\n')
                    one_session = {}
                    res = self.Get_data_with_type_of_record_M(line)
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

class Data_utils(object):

    #def Get_url_in_struct(self,url_id, url_info):
    #    #url_id,domain": "1084315", "time_passed": {}, "rank
    #    if (not isinstance(url['time_passed'], int)):
    #        url['tyme_passed'] = -1
    #    a = struct.pack('iiii', int(url_id),int(url_info['domain']),int(url_info['time_passed']),int(url['rank']))
    #    return a

    #def Get_serp_in_struct(self, serp):


    #def Get_data_to_bynary(self, session_file):
    #    #format serp_id:{},...,serp_id:{},user_id:<>,day:<>
    #    with open(session_file) as sessions, open(user_sessions_file, 'w') as user_session:
    #        for line in sessions:
    #            line = json.loads(line.strip())
    #            n_serps = len(line.keys()) - 2


    def Get_session_by_one_predicate(self, session_file, user_sessions_file, predicate):
        res = {}
        with open(session_file) as sessions, open(user_sessions_file, 'w') as user_session:
            for line_n,line in enumerate(sessions):
                if (line_n % 10**4 == 0):
                    print(line_n)
                line = json.loads(line.strip())
                if (line[predicate] not in res):
                    res[line[predicate]] = []
                res[line[predicate]].append(line_n)
            for key in res.keys():
                user_session.write(key + '\t' + ','.join(str(i) for i in res[key]) + '\n')

def pack(int_str):
    return bytes(struct.pack('i', int(int_str)))

def compress_json(line):
    parsed = json.loads(line.strip())
    compressed = b''
    compressed += pack(parsed['userId'])
    compressed += pack(parsed['day'])
    compressed += pack(len(parsed) - 2)
    for i in range(len(parsed) - 2):
        serp = parsed[str(i)]
        compressed += bytes(serp['typeOfRecord'])
        compressed += pack(serp['serpId'])
        compressed += pack(serp['QueryId'])
        compressed += pack(serp['time_passed'])
        list_of_terms = serp['listOfTerms']
        compressed += pack(len(list_of_terms))
        compressed += bytes(''.join([pack(x) for x in list_of_terms]))
        urls = serp['listOfUrlsAndDomains']
        compressed += pack(len(urls))
        for item in urls.items():
            compressed += pack(item[0])
            compressed += pack(item[1]['domain'])
            if not item[1]['time_passed'] == {}:
                compressed += pack(item[1]['time_passed'])
            else:
                compressed += pack(-1)
            compressed += pack(item[1]['rank'])
    return compressed

def compress_json_file(input_file, output_file):
    enumerator = 0
    with open(input_file) as reader, open(output_file, 'w') as writer:
        for line in reader:
            enumerator += 1
            if (enumerator%10**4 == 0):
                print enumerator
            compressed = compress_json(line)
            decompressed = session(compressed)
            writer.write(compressed)
            writer.write('\n')
            pass

def main():
    #data = Working_with_data(sys.argv[1])
    people = Data_utils()
    people.Get_session_by_one_predicate(sys.argv[1], sys.argv[2], 'userId')

if __name__ == "__main__":
    compress_json_file(
        input_file= '../../my_data/train',
        output_file= '../../my_data/train_bin')
