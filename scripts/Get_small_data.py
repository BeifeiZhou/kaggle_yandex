__author__ = 'anna'
import random
from get_items import *
n_training_days = 25
n_validation_days = 22

def Get_small_data(data_file):
    urls = []
    queries = []
    users = []
    with open(data_file) as data:
        for line_n,line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 == 0):
                if (int(line[3]) >= n_validation_days):
                    queries.append(int(line[2]))
                    users.append(int(line[0]))
            if (int(line[3]) >= n_validation_days):
                urls.append(int(line[4]))
    return [set(urls), set(queries), set(users)]

def Get_users(data_file, urls, queries):
    users = []
    with open(data_file) as data:
        for line_n,line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 == 0):
                if (int(line[2]) in queries):
                    users.append(int(line[0]))
            if (int(line[4]) in urls):
                users.append(int(line[0]))
    return set(users)

def Get_new_data(data_file,res_file, queries):
    push_line = False
    with open(data_file) as data, open(res_file, 'w') as res:
        for line_n,line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line1 = line.strip().split("\t")
            if (line_n%10 == 0):
                if (int(line1[0]) in queries):
                    push_line = True
                else:
                    push_line = False
            if (push_line):
                res.write(line)

def main():
    data_file = "../../big_data/trainW2V"
    urls_name, queries_name, users_name = Get_small_data(data_file)
    q_names_small = set([q for q in queries_name if random.randint(0,50) == 0])
    u_names_small = set([u for u in users_name if random.randint(0,50) == 0])
    Get_new_data(data_file,"../../big_data/trainW2V_small", u_names_small)

main()



