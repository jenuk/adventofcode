#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <unordered_map>
#include <cstdint>

std::vector<std::string> read_data(std::ifstream& file) {
    std::vector<std::string> result = {};
    std::string line;

    while (file >> line) {
        result.push_back(line);
    }

    return result;
}

int task1(std::vector<std::string>& data){
    int result = 0;

    for (int k=0; k<data.size(); k++) {
        std::vector<char> stack = {};

        for (int i=0; i<data[k].size(); i++) {
            if (data[k][i] == ')') {
                if (stack.back() == '(') {
                    stack.pop_back();
                } else {
                    result += 3;
                    break;
                }
            } else if (data[k][i] == ']') {
                if (stack.back() == '[') {
                    stack.pop_back();
                } else {
                    result += 57;
                    break;
                }
            } else if (data[k][i] == '}') {
                if (stack.back() == '{') {
                    stack.pop_back();
                } else {
                    result += 1197;
                    break;
                }
            } else if (data[k][i] == '>') {
                if (stack.back() == '<') {
                    stack.pop_back();
                } else {
                    result += 25137;
                    break;
                }
            } else {
                stack.push_back(data[k][i]);
            }
        }
    }

    return result;
}

int64_t task2(std::vector<std::string>& data) {
    std::unordered_map<char, int> values = {
        {'(', 1},
        {'[', 2},
        {'{', 3},
        {'<', 4},
    };
    std::vector<int64_t> scores;

    for (int k=0; k<data.size(); k++) {
        std::vector<char> stack = {};
        bool corrupted = false;

        for (int i=0; i<data[k].size(); i++) {
            if (data[k][i] == ')') {
                if (stack.back() == '(') {
                    stack.pop_back();
                } else {
                    corrupted = true;
                    break;
                }
            } else if (data[k][i] == ']') {
                if (stack.back() == '[') {
                    stack.pop_back();
                } else {
                    corrupted = true;
                    break;
                }
            } else if (data[k][i] == '}') {
                if (stack.back() == '{') {
                    stack.pop_back();
                } else {
                    corrupted = true;
                    break;
                }
            } else if (data[k][i] == '>') {
                if (stack.back() == '<') {
                    stack.pop_back();
                } else {
                    corrupted = true;
                    break;
                }
            } else {
                stack.push_back(data[k][i]);
            }
        }

        if (corrupted) {
            continue;
        }

        int64_t score = 0;
        for (int64_t i=stack.size()-1; i>=0; i--) {
            score = score*5 + values[stack[i]];
        }
        scores.push_back(score);
    }

    std::nth_element(scores.begin(), scores.begin()+scores.size()/2, scores.end());
    return scores[scores.size()/2];
}


int main() {
    std::ifstream file;
    file.open("input.txt");
    std::vector<std::string> data = read_data(file);
    file.close();

    int res1 = task1(data);
    int64_t res2 = task2(data);

    std::cout << res1 << "\n";
    std::cout << res2 << std::endl;

    return 0;
}
