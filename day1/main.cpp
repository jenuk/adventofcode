#include <string>
#include <iostream>
#include <fstream>
#include <array>

int task1(std::string filename) {
    std::ifstream file;
    file.open(filename);
    int prev, current;
    int result = 0;
    file >> prev;

    while (file >> current) {
        if (current > prev) {
            result++;
        }
        prev = current;
    }

    file.close();
    return result;
}


template <size_t N>
int task2(std::string filename) {
    std::ifstream file;
    file.open(filename);

    int result = 0;

    std::array<int, N> prev;
    for (size_t i=0; i<N; i++) {
        file >> prev[i];
    }

    int current;
    int pos=0;
    while (file >> current) {
        if (current > prev[pos]) {
            result++;
        }
        prev[pos] = current;
        pos = (pos+1)%N;
    }

    file.close();
    return result;
}

int main() {
    int result = task2<3>("input.txt");
    std::cout << "Number of increases: " << result << std::endl;
    return 0;
}
