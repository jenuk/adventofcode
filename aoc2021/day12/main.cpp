#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>


std::unordered_map<std::string, std::vector<std::string>> read_data(std::string filename) {
    std::ifstream file;
    file.open(filename);

    std::unordered_map<std::string, std::vector<std::string>> result;
    std::string line;
    while (file >> line) {
        int k = 0;
        for (;k < line.size(); k++) {
            if (line[k] == '-') {
                break;
            }
        }
        std::string a = line.substr(0, k);
        std::string b = line.substr(k+1);

        if (result.find(a) == result.end()) {
            result[a] = {b};
        } else {
            result[a].push_back(b);
        }

        if (result.find(b) == result.end()) {
            result[b] = {a};
        } else {
            result[b].push_back(a);
        }
    }

    file.close();

    return result;
}


int num_paths(const std::unordered_map<std::string, std::vector<std::string>>& graph,
              const std::string& pos,
              std::unordered_set<std::string> visited,
              bool double_cave) {
    if (pos[0] - 'a' >= 0) {
        visited.insert(pos);
    }

    int result = 0;
    std::string npos;

    for (int k=0; k<graph.at(pos).size(); k++) {
        npos = graph.at(pos)[k];
        if (npos == "end") {
            result++;
        } else if (visited.find(npos) != visited.end()) {
            if ((not double_cave) and (npos != "start")) {
                result += num_paths(graph, npos, visited, true);
            }
        } else {
            result += num_paths(graph, npos, visited, double_cave);
        }
    }
    return result;
}


int main() {
    std::unordered_map<std::string, std::vector<std::string>> graph = read_data("input.txt");

    int res1 = num_paths(graph, "start", {}, true);
    int res2 = num_paths(graph, "start", {}, false);

    std::cout << res1 << "\n"
              << res2 << std::endl;

    return 0;
}
