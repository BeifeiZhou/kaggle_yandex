__author__ = 'annasepliaraskaia'
from urls_as_summ_urls import *

def query_histogramm(query_by_users, res_file):
    res = [[q, len(query_by_users[q])] for q in query_by_users.keys()]
    res.sort(key=lambda x:-x[1])
    histogramm = []
    emissed_number = res[0][1]
    query_number = 0
    for i_n,i in enumerate(res):
        if (i_n % 10**5 == 0):
            print(i_n)
        if (emissed_number == i[1]):
            query_number += 1
        else:
            histogramm.append([emissed_number,query_number])
            emissed_number = i[1]
            query_number = 1
    histogramm.append([emissed_number, query_number])
    with open(res_file, 'w') as r:
        r.write("\n".join(str(i[0]) + "\t" + str(i[1]) for i in histogramm))

def main():

    data_file = "../../big_data/trainW2V"
    test_f = "../../big_data/trainW2V_small_test_q"
    train_f = "../../big_data/trainW2V_small_validation_q"

    queries_name = Get_queries(data_file)

    users_query = users_that_entered_query(data_file, queries_name)
    query_histogramm(users_query, "../../big_data/query_histogramm")
main()
