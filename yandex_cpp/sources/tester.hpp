#ifndef TESTER
#define TESTER
#include "utils.h"

class ExampleStrategy
{
public:
    vector<int> Calculate(const Query& query) const
    {
        return {1, 0, 2, 3, 4, 5, 6, 7, 8, 9};
    }
};

template<class Strategy>
class Tester
{
public:
    Tester(const string& file):
        initialStatistics(0), gotStatistics(0)
    {
        std::cout << "Tester: reading data ..." << std::endl;
        data = ReadDay(file);
    }

    void Calculate(Strategy& strategy)
    {
        size_t enumerator = 0;
        const vector<int> defaultRanging = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        for(const auto& item0 : data)
        {
            for (const auto& item1 : item0.second)
            {
                const Query& query = item1.second;
                vector<int> ranging = strategy.Calculate(query);
                if (ranging.size() > 0)
                {
                    updateStatistics(&initialStatistics, query, defaultRanging);
                }
                updateStatistics(&gotStatistics, query, ranging);
                if (enumerator++ % 100000 == 0)
                {
                    std::cout << "Tester: " << enumerator << " ..." << std::endl;
                }
            }
        }
    }

    void Print()
    {
        std::cout << "Basic ranker: " << initialStatistics << std::endl;
        std::cout << "Result ranker: " << gotStatistics << std::endl;
        std::cout << "Fraction: " << 100 * (gotStatistics / initialStatistics - 1) << "%s" << std::endl;
    }
private:
    void updateStatistics(double* cumulativeStat, const Query& query,
        const vector<int> ranging)
    {
        if (ranging.size() > 0 && query.type[ranging[0]] == 2)
        {
            *cumulativeStat += 1;
        }
    }

    double initialStatistics;
    double gotStatistics;
    DayData data;
};

#endif
