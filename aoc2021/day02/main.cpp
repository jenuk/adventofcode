#include <string>
#include <iostream>
#include <fstream>
#include <array>

int task1(std::ifstream& file) {
    int depth = 0;
    int horizontal = 0;
    std::string direction;
    int amount;

    while (file >> direction) {
        file >> amount;
        if (direction == "forward") {
            horizontal += amount;
        } else if (direction == "down") {
            depth += amount;
        } else if (direction == "up") {
            depth -= amount;
        } else {
            std::cerr << "unrecognized input '" << direction << "'" << std::endl;
        }
    }

    return depth*horizontal;
}

int task2(std::ifstream& file) {
    int aim = 0;
    int depth = 0;
    int horizontal = 0;
    std::string direction;
    int amount;

    while (file >> direction) {
        file >> amount;
        if (direction == "forward") {
            horizontal += amount;
            depth += aim * amount;
        } else if (direction == "down") {
            aim += amount;
        } else if (direction == "up") {
            aim -= amount;
        } else {
            std::cerr << "unrecognized input '" << direction << "'" << std::endl;
        }
    }

    return depth*horizontal;
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
