#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>

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

int task1(std::vector<std::vector<int>>& data){
    int result = 0;

    for (int i=0; i<data.size(); i++) {
        for (int j=0; j<data[i].size(); j++) {
            bool low = true;
            if (j - 1 >= 0) {
                low = low and data[i][j-1] > data[i][j];
            }
            if (j + 1 < data[i].size()) {
                low = low and data[i][j+1] > data[i][j];
            }
            if (i - 1 >= 0) {
                low = low and data[i-1][j] > data[i][j];
            }
            if (i + 1 < data.size()) {
                low = low and data[i+1][j] > data[i][j];
            }

            if (low) {
                result += data[i][j] + 1;
            }
        }
    }
    return result;
}

int task2(std::vector<std::vector<int>>& data) {
    std::vector<std::vector<int>> components;
    for (int i=0; i<data.size(); i++) {
        components.push_back(std::vector<int>(data[i].size(), -1));
    }
    std::vector<int> comp_size;
    std::vector<std::pair<int, int>> stack;
    
    int component = 0;
    int current_size;
    for (int i=0; i<data.size(); i++) {
        for (int j=0; j<data.size(); j++) {
            if (components[i][j] != -1 or data[i][j] == 9) {
                continue;
            }

            current_size = 0;
            stack.push_back(std::make_pair(i, j));
            while (not stack.empty()) {
                std::pair<int, int> p = stack.back();
                stack.pop_back();

                if (p.first < 0 or p.first >= data.size()
                        or p.second < 0 or p.second >= data[i].size()
                        or components[p.first][p.second] != -1
                        or data[p.first][p.second] == 9) {
                    continue;
                }

                components[p.first][p.second] = component;
                current_size++;

                stack.push_back(std::make_pair(p.first, p.second+1));
                stack.push_back(std::make_pair(p.first, p.second-1));
                stack.push_back(std::make_pair(p.first+1, p.second));
                stack.push_back(std::make_pair(p.first-1, p.second));
            }
            comp_size.push_back(current_size);
            component++;
        }
    }
    std::sort(comp_size.begin(), comp_size.end());
    return comp_size[comp_size.size()-1] * comp_size[comp_size.size()-2] * comp_size[comp_size.size()-3];
}


int main() {
    std::ifstream file;
    file.open("input.txt");
    std::vector<std::vector<int>> data = read_data(file);
    file.close();

    int res1 = task1(data);
    int res2 = task2(data);

    std::cout << res1 << "\n";
    std::cout << res2 << std::endl;

    return 0;
}
