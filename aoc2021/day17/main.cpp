#include <iostream>
#include <fstream>
#include <cmath>
#include <utility>

double traj(int p) {
    return -1./2. + std::sqrt(1./4. + 2.*p);
}


std::pair<int, int> range_y_steps(int y, int ly, int uy) {
    int top = (y*(y+1))/2;
    int n1 = std::ceil(traj(top - uy));
    int n2 = std::floor(traj(top - ly));
    return std::make_pair(n1, n2);
}


int task1(int lx, int ux, int ly, int uy) {
    int y = std::abs(ly); //assume 0 >= uy > ly

    std::pair<int, int> p;
    do { //could also do a binary search here
        y--;
        p = range_y_steps(y, ly, uy);
    } while (p.first > p.second);
     
    return (y*(y+1))/2;
}


bool simulate(int vx, int vy, int lx, int ux, int ly, int uy) {
    int posx = 0;
    int posy = 0;

    while ((posy >= ly) and (posx <= ux)) {
        if ((posy <= uy) and (posx >= lx)) {
            return true;
        }
        posx += vx;
        posy += vy;
        vx = vx > 0 ? vx-1 : 0;
        vy--;
    }

    return false;
}


int task2(int lx, int ux, int ly, int uy) {
    int result = 0;

    for (int x=0; x <= ux; x++) {
        for (int y=ly; y <= -ly; y++) {
            result += simulate(x, y, lx, ux, ly, uy);
        }
    }

    return result;
}


int main() {
    std::cout << "Example input:" << "\n"
              << "Task1: " << task1(20,   30, -10, - 5) << "\n"
              << "Task2: " << task2(20,   30, -10, - 5) << std::endl;
    std::cout << "My test input:" << "\n"
              << "Task1: " << task1(277, 318, -92, -53) << "\n"
              << "Task2: " << task2(277, 318, -92, -53) << std::endl;

    return 0;
}
