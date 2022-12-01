#include <iostream>
#include <fstream>
#include <vector>
#include <climits>

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

int task1(std::vector<int>& data) {
    int min = data[0];
    int max = data[0];
    for (int k=1; k<data.size(); k++) {
        if (data[k] > max) {
            max = data[k];
        } else if (data[k] < min) {
            min = data[k];
        }
    }

    int min_fuel = INT_MAX;
    for (int x=min; x<=max; x++) {
        int fuel = 0;
        for (int k=0; k<data.size(); k++) {
            fuel += std::abs(x - data[k]);
        }

        if (fuel < min_fuel) {
            min_fuel = fuel;
        } else {
            break;
        }
    }

    return min_fuel;
}


int gaus_sum(int n) {
    return (n * (n+1))/2;
}


int task2(std::vector<int> data) {
    int min = data[0];
    int max = data[0];
    for (int k=1; k<data.size(); k++) {
        if (data[k] > max) {
            max = data[k];
        } else if (data[k] < min) {
            min = data[k];
        }
    }

    int min_fuel = INT_MAX;
    for (int x=min; x<=max; x++) {
        int64_t fuel = 0;
        for (int k=0; k<data.size(); k++) {
            fuel += gaus_sum(std::abs(x - data[k]));
        }

        if (fuel < min_fuel) {
            min_fuel = fuel;
        } else {
            break;
        }
    }

    return min_fuel;
}


int main() {
    std::ifstream file;
    file.open("input.txt");

    std::vector<int> data = read_data(file);

    file.close();

    int res1 = task1(data);
    int res2 = task2(data);

    std::cout << "Task1: " << res1 << std::endl;
    std::cout << "Task2: " << res2 << std::endl;

    return 0;
}
