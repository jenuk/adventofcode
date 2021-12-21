#include <iostream>
#include <utility>
#include <unordered_map>
#include <cstdint>

int task1(int pos1, int pos2) {
    int score1 = 0;
    int score2 = 0;
    int dice = 1;
    bool current_player1 = true;

    while (score1 < 1000 and score2 < 1000) {
        if (current_player1) {
            pos1 = (pos1 + 3*(dice+1) - 1)%10 + 1;
            score1 += pos1;
        } else {
            pos2 = (pos2 + 3*(dice+1) - 1)%10 + 1;
            score2 += pos2;
        }
        dice += 3;
        current_player1 = !current_player1;
    }

    return (dice-1)*std::min(score1, score2);
}

std::pair<int64_t, int64_t> game(int pos1, int pos2, int score1, int score2, bool current_player1) {
    if (score1 >= 21) {
        return std::make_pair(1, 0);
    } else if (score2 >= 21) {
        return std::make_pair(0, 1);
    }

    std::unordered_map<int, int64_t> dice = {
        {4, 3}, // 1 + 1 + 2
        {5, 6}, // 1 + 1 + 3 = 2 + 2 + 1
        {7, 6}, // 2 + 2 + 3 = 3 + 3 + 1
        {8, 3}, // 3 + 3 + 2
        {3, 1}, // 1 + 1 + 1
        {6, 7}, // 2 + 2 + 2 = 1 + 2 + 3
        {9, 1}, // 3 + 3 + 3
    };

    std::pair<int64_t, int64_t> p = std::make_pair(0, 0);
    int next_pos1   = pos1;
    int next_pos2   = pos2;
    int next_score1 = score1;
    int next_score2 = score2;

    for (const auto& d : dice) {
        if (current_player1) {
            next_pos1   = (pos1 + d.first - 1)%10 + 1;
            next_score1 = score1 + next_pos1;
        } else {
            next_pos2   = (pos2 + d.first - 1)%10 + 1;
            next_score2 = score2 + next_pos2;
        }
        auto x    = game(next_pos1, next_pos2, next_score1, next_score2, !current_player1);
        p.first  += d.second * x.first;
        p.second += d.second * x.second;
    }

    return p;
}

int64_t task2(int pos1, int pos2) {
    auto p = game(pos1, pos2, 0, 0, true);
    return std::max(p.first, p.second);
}

int main(){
    int res1     = task1(8, 2);
    int64_t res2 = task2(8, 2);

    std::cout <<   "Task1: " << res1
              << "\nTask2: " << res2 << std::endl;
}
