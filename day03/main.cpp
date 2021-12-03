#include <string>
#include <iostream>
#include <fstream>
#include <vector>

int task1(std::ifstream& file) {
    std::string line;
    file >> line;
    int N = line.size();
    int n = 0;
    std::vector<int> count(N, 0);

    do {
        n++;
        for (int k=0; k<N; k++) {
            if (line[k] == '1') {
                count[k]++;
            }
        }
    } while (file >> line);

    int gamma = 0;
    int epsilon = 0;
    for (int k=0; k<N; ++k) {
        gamma = gamma << 1;
        epsilon = epsilon << 1;
        if (count[k] >= n/2) {
            gamma++;
        } else {
            epsilon++;
        }
    }

    return gamma*epsilon;
}

std::vector<std::string> read_lines(std::ifstream& file) {
    std::string line;
    std::vector<std::string> result;

    while (file >> line) {
        result.push_back(line);
    }

    return result;
}

int task2(std::ifstream& file) {
    std::vector<std::string> lines_co2 = read_lines(file);
    std::vector<std::string> lines_oxy(lines_co2);
    int co2 = 0;
    int oxy = 0;

    int N = lines_co2[0].size();

    for (int k=0; k<N; ++k) {
        std::vector<std::string> ones;
        std::vector<std::string> zeros;

        for (int i=0; i<lines_co2.size(); i++) {
            if (lines_co2[i][k] == '1') {
                ones.push_back(lines_co2[i]);
            } else {
                zeros.push_back(lines_co2[i]);
            }
        }

        co2 = co2 << 1;
        if (ones.size() >= zeros.size()) {
            co2++;
            lines_co2 = ones;
        } else {
            lines_co2 = zeros;
        }
    }

    for (int k=0; k<N; ++k) {
        std::vector<std::string> ones;
        std::vector<std::string> zeros;

        for (int i=0; i<lines_oxy.size(); i++) {
            if (lines_oxy[i][k] == '1') {
                ones.push_back(lines_oxy[i]);
            } else {
                zeros.push_back(lines_oxy[i]);
            }
        }

        oxy = oxy << 1;
        if ((zeros.size() == 0) or (ones.size() > 0 and ones.size() < zeros.size())) {
            oxy++;
            lines_oxy = ones;
        } else {
            lines_oxy = zeros;
        }
    }

    return oxy*co2;
}


int main() {
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
