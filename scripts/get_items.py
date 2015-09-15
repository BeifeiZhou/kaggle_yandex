

def Get_queries(data_file):
    queries_name = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            if (line_n%10 == 0):
                queries_name.append(int(line[2]))
    return set(queries_name)

def Get_urls(data_file):
    urls_name = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            urls_name.append(int(line[4]))
    return set(urls_name)

def Get_users(data_file):
    users = []
    with open(data_file) as data:
        for line_n, line in enumerate(data):
            if (line_n%10**6 == 0):
                print(line_n)
            line = line.strip().split("\t")
            users.append(int(line[0]))
    return set(users)
