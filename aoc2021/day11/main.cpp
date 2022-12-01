#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <utility>


std::vector<std::vector<int>> read_data(std::ifstream& file) {
    std::vector<std::vector<int>> result = {};
    std::string line;

    while (file >> line) {
        std::vector<int> vec;
        for (int k=0; k<line.size(); k++) {
            vec.push_back(line[k] - '0');
        }
        result.push_back(vec);
    }

    return result;
}


void increase(std::vector<std::vector<int>>& data,
              std::vector<std::pair<int, int>>& flashed,
              int i,
              int j) {
    //modifies data and flashed inplace
    if (i < 0 or i >= data.size()
            or j < 0 or j >= data[i].size()) {
        return;
    }

    data[i][j]++;

    if (data[i][j] == 10) {
        data[i][j] = -100;
        flashed.push_back(std::make_pair(i, j));

        for (int dx=-1; dx<=1; dx++) {
            for (int dy=-1; dy<=1; dy++) {
                increase(data, flashed, i+dx, j+dy);
            }
        }
    }
}


int task1(std::vector<std::vector<int>> data, int steps){
    int result = 0;
    std::vector<std::pair<int, int>> flashed;

    for (int k=0; k<steps; k++){
        for (int i=0; i<data.size(); i++) {
            for (int j=0; j<data[i].size(); j++){
                increase(data, flashed, i, j);
            }
        }
        result += flashed.size();

        for (int x=flashed.size()-1; x>=0; x--) {
            data[flashed[x].first][flashed[x].second] = 0;
            flashed.pop_back();
        }
    }

    return result;
}


int task2(std::vector<std::vector<int>> data) {
    std::vector<std::pair<int, int>> flashed;

    for (int k=1; true; k++){
        for (int i=0; i<data.size(); i++) {
            for (int j=0; j<data[i].size(); j++){
                increase(data, flashed, i, j);
            }
        }
        if (flashed.size() == data.size()*data[0].size()) {
            return k;
        }

        for (int x=flashed.size()-1; x>=0; x--) {
            data[flashed[x].first][flashed[x].second] = 0;
            flashed.pop_back();
        }
    }
}


int main() {
    std::ifstream file;
    file.open("input.txt");
    std::vector<std::vector<int>> data = read_data(file);
    file.close();

    int res1 = task1(data, 100);
    int res2 = task2(data);

    std::cout << res1 << "\n";
    std::cout << res2 << std::endl;

    return 0;
}
