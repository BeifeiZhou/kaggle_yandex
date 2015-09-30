#include "utils.h"
#include "tester.hpp"
#include <algorithm>
#include <cmath>


class Strategy
{
public:
    Strategy()
    {
        queryUrlParameters = Load("/tmp/query_url_parameters.txt");
        userUrlParameters = Load("/tmp/user_url_parameters.txt");
    }

    vector<int> Calculate(const Query& query)
    {
        for (size_t i = 0; i < 10; ++i)
        {
            if (Get(Get(userUrlParameters, query.person), query.urls[i], vector<double>(1, 0))[0] >= 1 - 1e-5)
            {
                return {};
            }
        }

        vector<double> prob(10);
        double currentProb = 1;
        for (size_t i = 0; i < 10; ++i)
        {
            vector<double>& pars = Get(Get(queryUrlParameters, query.id), query.urls[i]);
            if (pars.size() == 4 && pars[1] > 5) {
//                double click = pars[1] / (pars[1] + pars[2]);
//                prob[i] = currentProb * click * pars[0];
//                currentProb *= 1.0 - click * pars[3] / pars[1];
                prob[i] = currentProb * pars[1];
                currentProb *= 1.0 - pars[3] / pars[1];
            } else {
                prob[i] = prob[i-1]*0.9;
            }
        }
        vector<int> ranging = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        std::sort(ranging.begin(), ranging.end(), [&](int i, int j) { return prob[i] > prob[j]; } );
//        if (ranging[0] != 0)
//        {
//            for (size_t i = 0; i < 10; ++i)
//            {
//                vector<double>& pars = Get(Get(queryUrlParameters, query.id), query.urls[i]);
//                if (pars.size() == 4) {
//                    std::cout << prob[i] << " " << i << " " << ranging[i] << " " << query.type[i] << " :::: " << pars[0] << " " << pars[1] << " " << pars[2] << " " << pars[3] << std::endl;
//                } else {
//                    std::cout << prob[i] << " " << i << " " << ranging[i] << " " << query.type[i] << std::endl;
//                }
//            }
//            int i;
//            std::cin >> i;
//        }
        return ranging;
    }
};

void TryTester()
{
    Tester<Strategy> tester("/home/stepan/Anna/big_data/days/27.txt");
    Strategy strategy;
    tester.Calculate(strategy);
    tester.Print();
}

int main() 
{
// 1.
//    start = clock();
//    SeparateByDays("/home/stepan/Anna/big_data/trainW2V", "/home/stepan/Anna/big_data/days/");
//    end = clock();
//    std::cout << double(end - start) /  CLOCKS_PER_SEC << std::endl;

// 2.
    CalculateParameters("/home/stepan/Anna/big_data/days/");

// 3.
    TryTester();
}
