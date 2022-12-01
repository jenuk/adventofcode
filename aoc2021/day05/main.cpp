#include <iostream>
#include <fstream>
#include <regex>

int sign(int x) {
    return (x > 0) - (x < 0);
}

void parse_line(const std::string& line, std::array<int, 4>& coordinates) {
    const std::regex pattern("(\\d+),(\\d+) -> (\\d+),(\\d+)");
    std::smatch match;
    std::regex_match(line, match, pattern);

    for (int i=0; i < 4; ++i) {
        coordinates[i] = std::stoi(match[i+1].str());
    }
}


void extend_area(std::vector<std::vector<int>>& area, int i, int j) {
    for (int k=area.size(); k<=i; ++k) {
        area.push_back({});
    }

    for (int k=area[i].size(); k<=j; ++k) {
        area[i].push_back(0);
    }
}


int task1(std::ifstream& file) {
    std::vector<std::vector<int>> area = {};
    std::array<int, 4> coordinates;

    for (std::string line; getline(file, line);) {
        parse_line(line, coordinates);

        if (coordinates[0] == coordinates[2]) {
            int start = std::min(coordinates[1], coordinates[3]);
            int end   = std::max(coordinates[1], coordinates[3]);
            extend_area(area, coordinates[0], end);

            for (int t=start; t<=end; t++) {
                area[coordinates[0]][t]++;
            }
        } else if (coordinates[1] == coordinates[3]) {
            int start = std::min(coordinates[0], coordinates[2]);
            int end   = std::max(coordinates[0], coordinates[2]);
            for (int t=start; t<=end; t++) {
                extend_area(area, t, coordinates[1]);
                area[t][coordinates[1]]++;
            }
        }
    }

    int result = 0;
    for (int i=0; i < area.size(); i++) {
        for (int j=0; j < area[i].size(); j++) {
            if (area[i][j] >= 2) {
                result++;
            }
        }
    }

    return result;
}


int task2(std::ifstream& file) {
    std::vector<std::vector<int>> area = {};
    std::array<int, 4> coordinates;

    for (std::string line; getline(file, line);) {
        parse_line(line, coordinates);

        int dir_x = sign(coordinates[2] - coordinates[0]);
        int dir_y = sign(coordinates[3] - coordinates[1]);
        int num_steps = std::max(dir_x * (coordinates[2] - coordinates[0]), dir_y*(coordinates[3] - coordinates[1]));
        
        for (int t=0; t<=num_steps; t++){
            extend_area(area, dir_x*t+coordinates[0], dir_y*t+coordinates[1]);
            area[dir_x*t + coordinates[0]][dir_y*t + coordinates[1]]++;
        }
    }

    int result = 0;
    for (int i=0; i < area.size(); i++) {
        for (int j=0; j < area[i].size(); j++) {
            if (area[i][j] >= 2) {
                result++;
            }
        }
    }

    return result;
}


int main(){
    std::ifstream file;
    file.open("input.txt");

    int result1 = task1(file);

    file.clear();
    file.seekg(0, std::ios::beg);

    int result2 = task2(file);

    file.close();
    
    std::cout << "Result of task1: " << result1 << "\n";
    std::cout << "Result of task2: " << result2 << std::endl;

    return 0;
}
