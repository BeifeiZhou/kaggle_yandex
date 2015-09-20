from linear_regression_and_hash_features import *

class Train_model(object):
    def __init__(self, train_file, test_file, n_bins):
        self.train = train_file
        self.test = open(test_file)
        self.n_bins = n_bins
        self.learner = Linear_regression(0.1,1.,1.,1.)

    def train_by_one_file(self, file_index):
        with open(self.train) as file:
            for i,line in enumerate(file):
                if (i%10**6 == 0):
                    print(i)
                line = line.strip().split('\t')
                ex = [float(feature) for feature in line[:-1]]
                ex = HashFeatures(ex, [str(i) for i in range(len(ex))], self.n_bins)
                truth = float(int(line[-1]) >= 2)
                self.learner.one_step(ex, truth)

    def trainer(self):
        self.train_by_one_file(0)
        #self.train_by_one_file(1)

    def run_test(self, test_file):
        session = []
        correct_answer = 0
        n_answers = 0
        with open(test_file, 'w') as res_file:
            for line_n,line in enumerate(self.test):
                if (line_n%10**6 == 0):
                    print(line_n)
                line = line.strip().split('\t')
                #if len(line[0].split('_')) > 1:
                if (line_n%10 == 0):
                    if (len(session) > 0):
                        results = []
                        for s in session:
                            results.append([s[0], self.learner.res(HashFeatures(s[1], [str(i) for i in range(len(s[1]))], self.n_bins)), s[2]])
                        results.sort(key=lambda x:-x[1])
                        urls_with_max_score = [r for r in results if abs(r[1] - results[0][1]) < 1e-10]
                        urls_with_max_score.sort(key = lambda x:x[0])
                        max_truth = max(r[2] for r in results)
                        if (int(max_truth) == int(urls_with_max_score[0][2])):
                            correct_answer += 1
                        n_answers += 1
                    session = []
                    if (len(line) > 1):
                        session.append([line_n%10,[float(i) for i in line[:-1]], float(line[-1])])
                else:
                    session.append([line_n%10, [float(i) for i in line[:-1]], float(line[-1])])
        return [correct_answer, n_answers]

tr = Train_model("my_validation", "my_test", 2**30)
tr.trainer()
print(tr.run_test("../../data/res"))