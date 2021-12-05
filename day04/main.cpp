#include <iostream>
#include <fstream>
#include <regex>
#include <vector>
#include <utility>


class Bingo {
    public:
        Bingo() : won(false), score(0) {
            for (int i=0; i<5; i++) {
                this->_data.push_back({});
                this->_marked.push_back({});
                for (int j=0; j<5; j++) {
                    this->_data[i].push_back(0);
                    this->_marked[i].push_back(false);
                }
            }
        }
        std::pair<bool, int> mark(int n) {
            if (this->won) {
                return std::make_pair(false, 0);
            }
            for (int i=0; i<5; i++) {
                for (int j=0; j<5; j++) {
                    if (this->_data[i][j] == n) {
                        this->_marked[i][j] = true;
                        this->check_win(i, j);
                        return std::make_pair(this->won, this->score);
                    }
                }
            }
            return std::make_pair(false, 0);
        }

        void check_win(int i, int j) {
            if (this->won) {
                return;
            }

            int row_sum = 0;
            int col_sum = 0;
            for (int k=0; k<5; k++) {
                row_sum += this->_marked[i][k];
                col_sum += this->_marked[k][j];
            }

            if (row_sum == 5 or col_sum == 5) {
                this->won = true;
                this->score = 0;
                for (int n=0; n<5; ++n) {
                    for (int m=0; m<5; ++m) {
                        this->score += (1 - this->_marked[n][m]) * this->_data[n][m];
                    }
                }
                this->score *= this->_data[i][j];
            }
        }

        friend std::istream& operator>>(std::istream& is, Bingo& bingo);
        friend std::ostream& operator<<(std::ostream& os, Bingo& bingo);

    private:
        std::vector<std::vector<int>> _data;
        std::vector<std::vector<bool>> _marked;
        int score;
        bool won;
};


std::ostream& operator<<(std::ostream& os, Bingo& bingo) {
    for (int i=0; i<5; i++) {
        for (int j=0; j<5; j++) {
            os << bingo._data[i][j] << " ";
        }
        os << "\n";
    }

    return os;
}

std::istream& operator>>(std::istream& is, Bingo& bingo) {
    for (int i=0; i<5; i++) {
        for (int j=0; j<5; j++) {
            is >> bingo._data[i][j];
        }
    }

    return is;
}

std::pair<std::vector<int>, std::vector<Bingo>> read_data(std::ifstream& file) {
    std::string line;
    file >> line;
    const std::regex pattern("(\\d+)(,|$)");
    std::smatch match;
    std::vector<int> called;
    while (std::regex_search(line, match, pattern)) {
        called.push_back(std::stoi(match[1].str()));
        line = match.suffix();
    }

    std::vector<Bingo> bingos;
    Bingo bingo;
    while (file >> bingo) {
        bingos.push_back(bingo);
        bingo = Bingo();
    }
    
    return std::make_pair(called, bingos);
}


std::vector<int> calculate_scores(const std::vector<int>& nums, std::vector<Bingo>& bingos) {
    std::vector<int> scores;
    for (int k=0; k<nums.size(); k++) {
        for (int x=0; x<bingos.size(); x++) {
            auto pair = bingos[x].mark(nums[k]);
            if (pair.first) {
                scores.push_back(pair.second);
            }
        }
    }
    return scores;
}

int main(){
    std::ifstream file;
    file.open("input.txt");

    auto data = read_data(file);

    file.close();

    std::vector<int> called = data.first;
    std::vector<Bingo> bingos = data.second;

    std::vector<int> scores = calculate_scores(called, bingos);
    
    std::cout << "Task1: " << scores.front() << "\n"
              << "Task2: " << scores.back()  << std::endl;
    
    return 0;
}
