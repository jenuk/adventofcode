#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <utility>


std::pair<std::vector<std::vector<bool>>, std::vector<std::pair<char, int>>> read_data(const std::string& filename) {
    std::vector<std::vector<bool>>    field = {{false}};
    std::vector<std::pair<char, int>> operations;

    std::ifstream file;
    file.open(filename);
    
    for (std::string line; std::getline(file, line);) {
        if (line[0] == 'f') {
            operations.push_back(std::make_pair(line[11], std::stoi(line.substr(13))));
        } else if (line.size() > 0) {
            int k=0;
            while (k < line.size() and line[k] != ',') {
                k++;
            }
            int x = std::stoi(line.substr(0, k));
            int y = std::stoi(line.substr(k+1));

            while (x >= field.size()) {
                field.push_back(std::vector<bool>(field[0].size(), false));
            }

            if (y >= field[0].size()) {
                for (int k=0; k<field.size(); k++) {
                    std::vector<bool> v(y - field[k].size()+1, false);
                    field[k].insert(field[k].end(), v.begin(), v.end());
                }
            }

            field[x][y] = true;
        }
    }

    file.close();
    return std::make_pair(field, operations);

}


void print(std::vector<std::vector<bool>> field) {
    for (int y=0; y < field[0].size(); y++) {
        for (int x=0; x < field.size(); x++) {
            std::cout << (field[x][y] ? '#' : '.');
        }
        std::cout << "\n";
    }
    std::cout << std::endl;
}


void apply_folds(std::vector<std::vector<bool>>& field, const std::vector<std::pair<char, int>>& ops) {
    int axis;
    for (int k=0; k < ops.size(); k++) {
        axis = ops[k].second;
        if (ops[k].first == 'y') {
            for (int x=0; x<field.size(); x++) {
                for (int y=axis+1; y<field[x].size(); y++) {
                    if (field[x][y]) {
                        field[x][2*axis-y] = true;
                        field[x][y] = false;
                    }
                }
                field[x].erase(field[x].begin()+axis, field[x].end());
            }
        } else {
            for (int x=axis+1; x<field.size(); x++) {
                for (int y=0; y<field[x].size(); y++) {
                    if (field[x][y]) {
                        field[2*axis - x][y] = true;
                        field[x][y] = false;
                    }
                }
            }
            field.erase(field.begin()+axis, field.end());
        }
        
        if (k == 0) {
            int res1 = 0;
            for (int x=0; x<field.size(); x++) {
                for (int y=0; y<field[x].size(); y++) {
                    res1 += field[x][y];
                }
            }
            std::cout << "Task 1: " << res1 << std::endl;
        }
    }
}


int main() {
    auto inp = read_data("input.txt");

    apply_folds(inp.first, inp.second);
    std::cout << "Task 2:" << std::endl;
    print(inp.first);
}
