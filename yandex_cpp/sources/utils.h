#ifndef UTILS
#define UTILS

#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <fstream>
#include <ctime>
#include <cstdlib>

using std::vector;
using std::unordered_map;
using std::string;
using std::ifstream;
using std::ofstream;

struct Query
{
    size_t id;
    size_t person;
    vector<size_t> urls;
    vector<int> type;

    Query() : urls(10, -1), type(10, -1) {}
};


typedef unordered_map<size_t, unordered_map<size_t, Query> > DayData;
typedef unordered_map<size_t, unordered_map<size_t, size_t> > UUmap;
typedef unordered_map<size_t, unordered_map<size_t, vector<double> > > Parameters;

extern Parameters queryUrlParameters;
extern Parameters userUrlParameters;

template<class Key, class Value>
Value& Get(unordered_map<Key, Value>& data, const Key& key, Value def = Value())
{
    if (data.find(key) == data.end()) {
        data[key] = def;
    }
    return data[key];
}

void SeparateByDays(const string& file, const string& outFolder);

DayData ReadDay(const string& file);

void CalculateParameters(const string& folder);

void Save(const string& file, const Parameters& parameters);

Parameters Load(const string& file);

#endif
