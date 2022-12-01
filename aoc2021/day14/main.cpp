#include <iostream>
#include <fstream>
#include <unordered_map>
#include <utility>
#include <cstdint>

typedef std::unordered_map<std::string, char> Cookbook;


std::pair<Cookbook, std::string> read_data(std::string filename) {
    std::ifstream file;
    file.open(filename);
    std::string elements;
    std::getline(file, elements);

    Cookbook map;

    std::string line;
    std::getline(file, line);
    while (std::getline(file, line)) {
        map[line.substr(0,2)] = line[6];
    }

    file.close();

    return std::make_pair(map, elements);
}


int64_t task1(Cookbook& map, std::string elements, int steps) {
    std::string next;
    for (int k=0; k<steps; k++) {
        next = elements[0];
        for (int64_t i=1; i<elements.size(); i++) {
            next += map[elements.substr(i-1, 2)];
            next += elements[i];
        }
        elements = next;
    }

    std::unordered_map<char, int64_t> counts;
    for (int64_t i=0; i<elements.size(); i++) {
        if (counts.find(elements[i]) == counts.end()) {
            counts[elements[i]] = 1;
        } else {
            counts[elements[i]]++;
        }
    }

    int64_t max, min;
    min = max = counts[elements[0]];
    for (const auto& el : counts) {
        if (el.second > max) {
            max = el.second;
        } else if (el.second < min) {
            min = el.second;
        }
    }

    return max - min;
}


int64_t task2(Cookbook& map, std::string elements, int steps) {
    std::unordered_map<std::string, int64_t> pair_counts;
    for (int i=0; i<elements.size()-1; i++) {
        if (pair_counts.find(elements.substr(i, 2)) == pair_counts.end()) {
            pair_counts[elements.substr(i, 2)] = 1;
        } else {
            pair_counts[elements.substr(i, 2)]++;
        }
    }

    std::unordered_map<std::string, int64_t> next_counts;
    std::string a;
    for (int k=0; k<steps; k++) {
        next_counts.clear();
        for (const auto& p : pair_counts) {
            a  = p.first[0]; 
            a += map[p.first];
            if (next_counts.find(a) == next_counts.end()) {
                next_counts[a]  = p.second;
            } else {
                next_counts[a] += p.second;
            }
            a  = map[p.first];
            a += p.first[1];
            if (next_counts.find(a) == next_counts.end()) {
                next_counts[a]  = p.second;
            } else {
                next_counts[a] += p.second;
            }
        }
        std::swap(next_counts, pair_counts);
    }

    std::unordered_map<char, int64_t> counts;
    for (const auto& p : pair_counts) {
        if (counts.find(p.first[0]) == counts.end()) {
            counts[p.first[0]] = p.second;
        } else {
            counts[p.first[0]] += p.second;
        }
    }
    counts[elements[elements.size() - 1]]++;

    int64_t max, min;
    min = max = counts[elements[0]];
    for (const auto& el : counts) {
        if (el.second > max) {
            max = el.second;
        } else if (el.second < min) {
            min = el.second;
        }
    }

    return max - min;
}


int main() {
    std::pair<Cookbook, std::string> data = read_data("input.txt");

    int64_t res1 = task1(data.first, data.second, 10);
    int64_t res2 = task2(data.first, data.second, 40);

    std::cout << "Task1: " << res1 << "\n"
              << "Task2: " << res2 << std::endl;

    return 0;
}
