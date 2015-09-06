import sys
import linecache
import json

def Click_types(time, rang, last_click_rang):
    if last_click_rang == -1:
       return -1
    if time == {} or time < 0:
       if rang < last_click_rang:
          return -2
       else:
          return -1
    if rang != last_click_rang:
       if (time < 50):
          return 0
       if (time < 300):
          return 1
    return 2

def Get_new_format_in_serp(old_serp):
    urls = []
    serp = old_serp
    us = serp['listOfUrlsAndDomains']
    for url in us.keys():
        urls.append([int(us[url]['rang']), url, us[url]])
    urls.sort(key = lambda x:x[0])
    rang_last_click = -1
    for url in urls:
        if url[2]['time_passed'] != {}:
           rang_last_click = url[0]
    if rang_last_click < 0:
       for u in serp['listOfUrlsAndDomains'].keys():
           serp['listOfUrlsAndDomains'][u]['type'] = -1
    serp['rang_last_click'] = rang_last_click
    return serp

    last_time = urls[rang_last_click][2]['time_passed']
    for u in serp['listOfUrlsAndDomains'].keys():
        serp['listOfUrlsAndDomains'][u]['type'] = -1
    url = urls[rang_last_click]
    while url[0] >= 1:
       time = serp['listOfUrlsAndDomains'][urls[url[0] - 1][1]]['time']        
       if (time == {}):
           serp['listOfUrlsAndDomains'][urls[url[0]-1][1]]['type'] = -2
       else:
           serp['listOfUrlsAndDomains'][urls[url[0]-1][1]]['type'] = Click_types(last_time-time, url[0]-1,rang_last_click)
           last_time = time
       url = urls[url[0]-1]
    return serp        
 
def Get_features(elements, data_file):
    n_outcomes = 5
    res = []
    counts_outcome = {}
    i = -2
    while i < 3:
        counts_outcome[i] = 0
        i += 1
    for el in elements:
        serp = Get_new_format_in_serp(data[el['session']][el['serp_id']])
        counts_outcome[serp[el['listofUrlsAndDomains']][el['url']]['type']] += 1
    for key in counts_outcome.keys():
        res.append((counts_outcome[key] + 1.) / (len(elements) + n_outcomes))
    
        return res 
        
        
 
def read_data(data_file):
    data = []
    with open(data_file) as d_f:
         data = d_f.read().split('\n')
    return data

def get_data(data_file, lines):
    res = []
    with open(data_file) as d_f:
        for i,line in enumerate(d_f):
            if i in lines:
                res.append(line.strip())
    return res

class User_specific_features(object):

      def get_one_domain_urls(self, user_sessions, data_file):
          domains = {}

          data = data_file + str(user_sessions[0]/10**6)
          sessions_in_file = [s%10**6 for s in user_sessions]
          user_data = get_data(data, sessions_in_file)

          for i,session in enumerate(user_sessions):
              session = int(session)


              s = json.loads(user_data[i])
              for key in s.keys():
                  if key != 'userId' and key != 'day':
                      list_of_urls = s[key]['listOfUrlsAndDomains']
                      for url_key in list_of_urls.keys():
                          url = list_of_urls[url_key]
                          if url['domain'] not in domains:
                              domains[url['domain']] = []
                          res = {}
                          res['day'] = s['day']
                          res['query'] = set(s[key]['listOfTerms'])
                          res['time_passed'] = url['time_passed']
                          res['rank'] = url['rank']
                          res['session'] = session
                          res['serp_id'] = key
                          res['url'] = url_key
                          domains[url['domain']].append(res)
          return domains
       
      def get_query_filter(self, domain):
          n_urls = len(domain) 
          for first_url in domain:
              same_queries = []
              superset_queries = []
              subset_queries = []
              all_queries = []
              for second_url in  domain:
                  if first_url['query'] == second_url['query']:
                     same_queries.append(second_url)
                  elif first_url['query'].issuperset(second_url['query']):
                     superset_queries.append(second_url)
                  elif first_url['query'].issubset(second_url['query']):
                     subset_queries.append(second_url)
              Get_features(same_queries)
                   

      def features_for_one_user(self, user_sessions_file, data_file):
          aggregation = {}
          with open(user_sessions_file) as u_s:
              for line in u_s:
                  line = line.strip().split('\t')
                  user = line[0]
                  user_session = [int(i) for i in line[1].split(',')]
                  domains = self.get_one_domain_urls(user_session, data_file)
                  for domain in domains.keys():
                      self.get_query_filter(domains[keys])
          
us = User_specific_features()
us.features_for_one_user('../../my_data/users_sessions', '../../my_data/train_by_lines/')
#last_file = 0
#new_file = '../../my_data/train_by_lines_bin/'
#with open('../../my_data/train_bin') as train:
#    for i,line in enumerate(train):
#        if (i%10**4==0):
#            print(i)
#        if (i%10**6==0):
#            i += 1
#            fp = open(new_file+str(i/10**6), 'w')
#        fp.write(line)