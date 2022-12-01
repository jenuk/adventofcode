#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <unordered_map>
#include <cstdint>


std::pair<int64_t, int64_t> task(std::string filename){
    int64_t result1 = 0;
    int64_t result2 = 0;

    std::unordered_map<char, char> pairs = {
        {'(', ')'},
        {'[', ']'},
        {'{', '}'},
        {'<', '>'},
    };
    
    std::unordered_map<char, int> values = {
        {'(',     1},
        {'[',     2},
        {'{',     3},
        {'<',     4},
        {')',     3},
        {']',    57},
        {'}',  1197},
        {'>', 25137},
    };
    std::vector<int64_t> scores;

    std::ifstream file;
    file.open("input.txt");

    std::string line;
    std::vector<char> stack;
    bool corrupted;

    while (file >> line) {
        stack.clear();
        corrupted = false;

        for (int i=0; i<line.size(); i++) {
            if (line[i] == '(' or line[i] == '['
                    or line[i] == '{' or line[i] == '<') {
                stack.push_back(line[i]);
            } else {
                if (pairs[stack.back()] == line[i]) {
                    stack.pop_back();
                } else {
                    result1 += values[line[i]];
                    corrupted = true;
                    break;
                }
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
    file.close();

    std::nth_element(scores.begin(), scores.begin()+scores.size()/2, scores.end());
    result2 = scores[scores.size()/2];

    return std::make_pair(result1, result2);
}


int main() {
    std::pair<int64_t, int64_t> res = task("input.txt");

    std::cout << res.first << "\n";
    std::cout << res.second << std::endl;

    return 0;
}
