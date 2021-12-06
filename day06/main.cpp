#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>

std::vector<int> read_data(std::ifstream& file) {
    int k;
    char delimeter;
    std::vector<int> result;

    while (file >> k >> delimeter) {
        result.push_back(k);
    }
    result.push_back(k);

    return result;
}

int64_t breed(std::vector<int>& data, int days) {
    std::vector<int64_t> cycle(7, 0);
    std::vector<int64_t> newborn(3, 0);

    for (int k=0; k<data.size(); k++) {
        cycle[data[k]]++;
    }

    int pos_cycle = 0;
    int pos_newborn = 0;
    while (days > 0) {
        newborn[(pos_newborn+2)%3] += cycle[pos_cycle];
        cycle[pos_cycle] += newborn[pos_newborn];
        newborn[pos_newborn] = 0;
        pos_cycle = (pos_cycle+1)%7;
        pos_newborn = (pos_newborn+1)%3;
        days--;
    }

    int64_t result = 0;
    for (int k=0; k<cycle.size(); ++k) {
        result += cycle[k];
    }
    for (int k=0; k<newborn.size(); ++k) {
        result += newborn[k];
    }


    return result;
}


int main() {
    std::ifstream file;
    file.open("input.txt");

    std::vector<int> data = read_data(file);

    file.close();

    int64_t res1 = breed(data, 80);
    int64_t res2 = breed(data, 256);

    std::cout << "Task1: " << res1 << std::endl;
    std::cout << "Task2: " << res2 << std::endl;

    return 0;
}
