#include "utils.h"

Parameters queryUrlParameters;
Parameters userUrlParameters;

void SeparateByDays(const string& file, const string& outFolder)
{
    vector<ofstream*> outs;
    for (size_t i = 0; i < 30; ++i)
    {
        string toOpen = outFolder + std::to_string(i) + ".txt";
        outs.emplace_back(new ofstream(toOpen, std::ios::binary | std::ios::out));
    }
    ifstream input(file);
    size_t person, session, query, day, url, rank;
    int type;
    size_t enumerator = 0;
    while(!input.eof())
    {
        input >> person >> session >> query >> day >> url >> type >> rank;
        ofstream* out = outs[day];
        out->write((char*)&person, sizeof(size_t));
        out->write((char*)&session, sizeof(size_t));
        out->write((char*)&query, sizeof(size_t));
        out->write((char*)&url, sizeof(size_t));
        out->write((char*)&type, sizeof(int));
        out->write((char*)&rank, sizeof(size_t));
        if (++enumerator % 100000 == 0) {
            std::cout << enumerator << std::endl;
        }
    }
    input.close();
    for (size_t i = 0; i < 30; ++i)
    {
        outs[i]->close();
        delete outs[i];
    }
}

DayData ReadDay(const string& file)
{
    DayData data;
    ifstream input(file, std::ios::binary | std::ios::in);
    size_t person, session, query, url, rank;
    int type;
    size_t enumerator = 0;
    while(!input.eof())
    {
        input.read((char*)&person, sizeof(size_t));
        input.read((char*)&session, sizeof(size_t));
        input.read((char*)&query, sizeof(size_t));
        input.read((char*)&url, sizeof(size_t));
        input.read((char*)&type, sizeof(int));
        input.read((char*)&rank, sizeof(size_t));
        Query& addedQuery = Get(Get(data, person), session);
        addedQuery.id = query;
        addedQuery.person = person;
        addedQuery.urls[rank] = url;
        addedQuery.type[rank] = type;
        if (++enumerator % 100000 == 0) {
            std::cout << enumerator << std::endl;
        }
    }
    input.close();
    return data;
}

void CalculateParameters(const DayData& data)
{
    for(const auto& item0 : data)
    {
        for (const auto& item1 : item0.second)
        {
            const Query& query = item1.second;

            bool found = false;
            for (size_t i = 0; i <= query.type.size(); ++i)
            {
                vector<double>& vec = Get(Get(userUrlParameters, query.person), query.urls[i], vector<double>(1));
                if (vec[0] > 0) found = true;
                if (query.type[i] == 2) {
                    vec[0] += 1;
                } else if (vec[0] < 0.5) {
                    Get(userUrlParameters, query.person).erase(query.urls[i]);
                }
            }
            // if (found) continue;

            size_t maxIndex = 0;
            int maxElem = query.type[0];
            for (size_t i = 0; i < 10; ++i)
            {
                if (query.type[i] >= maxElem) {
                    maxIndex = i;
                    maxElem = query.type[i];
                }
            }
            if (maxElem != 2) continue;
            for (size_t i = 0; i <= maxIndex; ++i)
            {
                vector<double>& vec = Get(Get(queryUrlParameters, query.id), query.urls[i], vector<double>(4));
                vec[0] += 1;
                if (query.type[i] == 2) {
                    vec[1] += 1;
                } else {
                    vec[2] += 1;
                }
                if (i == maxIndex)
                {
                    vec[3] += 1;
                }
            }
        }
    }
}

void CalculateParameters(const string& folder)
{
    clock_t start, end;
    for(size_t i = 1; i <= 26; ++i)
    {
        start = clock();
        string file = folder + std::to_string(i) + ".txt";
        DayData data = ReadDay(file);
        end = clock();
        std::cout << i << " reading: " << double(end - start) /  CLOCKS_PER_SEC << std::endl;
        start = clock();
        CalculateParameters(data);
        end = clock();
        std::cout << i << " calculations: " << double(end - start) /  CLOCKS_PER_SEC << std::endl;
    }
    Save("/tmp/query_url_parameters.txt", queryUrlParameters);
    Save("/tmp/user_url_parameters.txt", userUrlParameters);
}

void binary_example()
{
    ofstream out;
    out.open("/tmp/del1", std::ios::binary | std::ios::out);
    int i = 10000;
    out.write((char*)&i, sizeof(int));
    out.write((char*)&i, sizeof(int));
    out.write((char*)&i, sizeof(int));
    out.close();

    ifstream in;
    in.open("/tmp/del1", std::ios::binary | std::ios::in);
    int iii1, iii2, iii3;
    in.read((char*)&iii1, sizeof(int));
    in.read((char*)&iii2, sizeof(int));
    in.read((char*)&iii3, sizeof(int));
    in.close();
}

void Save(const string& file, const Parameters& parameters)
{
    ofstream out(file);
    size_t size = 0;
    for(const auto& item0 : parameters)
    {
        size += item0.second.size();
    }
    out << size << " " << parameters.begin()->second.begin()->second.size() << std::endl;
    for(const auto& item0 : parameters)
    {
        for (const auto& item1 : item0.second)
        {
            out << item0.first << " " << item1.first;
            for (double feature : item1.second)
            {
                out << " " << feature;
            }
            out << std::endl;
        }
    }
    out.close();
}

Parameters Load(const string& file)
{
    Parameters parameters;
    ifstream in(file);
    size_t size, numFeat;
    in >> size >> numFeat;
    for (size_t i = 0; i < size; ++i)
    {
        size_t first, second;
        in >> first >> second;
        vector<double>& features = Get(Get(parameters, first), second, vector<double>(numFeat));
        for (size_t j = 0; j < numFeat; ++j) in >> features[j];
    }
    in.close();
    return parameters;
}


