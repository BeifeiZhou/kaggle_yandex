from linear_regression_and_hash_features import *

class Train_model(object):
    def __init__(self, train_file, my_test_file, test_file):
        self.train = open(train_file)
        self.test = open(test_file)
        self.learner = Linear_regression(0.1,1.,1.,1.)

    def train_by_one_file(self, file_index):
        file = self.train
        if (file_index == 1):
            file = self.my_test
        for i,line in enumerate(file):
            if (i%10**6 == 0):
                print(i)
            line = line.strip().split('\t')
            ex = [int(feature) for feature in line[:-1]]
            truth = float(int(line[-1]) >= 2)
            self.learner.one_step(ex, truth)
        file.close()

    def trainer(self):
        self.train_by_one_file(0)
        #self.train_by_one_file(1)

    def run_test(self, test_file):
        session = []
        session_id = ''
        with open(test_file, 'w') as res_file:
            res_file.write("SessionID,URLID\n")
            for line_n,line in enumerate(self.test):
                if (line_n > 10**6):
                    break
                if (line_n%10**6 == 0):
                    print(line_n)
                line = line.strip().split('\t')
                #if len(line[0].split('_')) > 1:
                if (line_n%10 == 0):
                    if (len(session) > 0):
                        results = []
                        for s in session:
                            results.append([s[0], self.learner.res(s[1]), s[2]])
                        results.sort(key=lambda x:-x[1])
                        for r in results:
                            res_file.write(str(r[0]) + "," + str(r[1]) + "," + str(r[2])+"\n")
                    session = []
                    if (len(line) > 1):
                        session.append([line_n/10,[int(i) for i in line[:-1]], line[-1]])
                else:
                    session.append([line_n/10, [int(i) for i in line[:-1]], line[-1]])

#tr = Train_model("../../data/my_train", "../../data/my_test", "../../data/my_test")
#tr.trainer()
#tr.run_test("../../data/res")