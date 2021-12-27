#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <utility>
#include <cassert>
#include <cstdint>


struct Vek {
    int x;
    int y;
    int z;

    bool operator<=(const Vek& other) const {
        return (this->x <= other.x) and
               (this->y <= other.y) and
               (this->z <= other.z);
    }
};

std::ostream& operator<<(std::ostream& os, const Vek& v) {
    os << "{" << v.x << ", " << v.y << ", " << v.z << "}";
    return os;
}

class Cube {
    public:
        Cube(const Vek min, const Vek max) : min(min), max(max) {
            assert(min <= max);
        }

        bool test_intersect(const Cube& other) const {
           return (this->min <= other.max) and (other.min <= this->max);
        }

        Cube intersection(const Cube& other) const {
            Vek a{std::max(this->min.x, other.min.x),
                  std::max(this->min.y, other.min.y),
                  std::max(this->min.z, other.min.z)};
            
            Vek b{std::min(this->max.x, other.max.x),
                  std::min(this->max.y, other.max.y),
                  std::min(this->max.z, other.max.z)};

            // make a <= b
            b = Vek{std::max(a.x, b.x), std::max(a.y, b.y), std::max(a.z, b.z)};

            return Cube(a, b);
        }

        std::vector<Cube> minus(const Cube& other) const {
            if (not this->test_intersect(other)) {
                return {(*this)};
            }
            Cube intersect = this->intersection(other);

            std::vector<Cube> cubes;
            Vek a = this->min;
            Vek b = this->max;

            if (this->min.z < intersect.min.z) {
                b.z = intersect.min.z;
                cubes.push_back(Cube(a, b));
                b.z = this->max.z;
            }
            if (intersect.max.z < this->max.z) {
                a.z = intersect.max.z;
                cubes.push_back(Cube(a, b));
            }
            a.z = intersect.min.z;
            b.z = intersect.max.z;

            if (this->min.y < intersect.min.y) {
                b.y = intersect.min.y;
                cubes.push_back(Cube(a, b));
                b.y = this->max.y;
            }
            if (intersect.max.y < this->max.y) {
                a.y = intersect.max.y;
                cubes.push_back(Cube(a, b));
            }
            a.y = intersect.min.y;
            b.y = intersect.max.y;

            if (this->min.x < intersect.min.x) {
                b.x = intersect.min.x;
                cubes.push_back(Cube(a, b));
                b.x = this->max.x;
            }
            if (intersect.max.x < this->max.x) {
                a.x = intersect.max.x;
                cubes.push_back(Cube(a, b));
            }

            return cubes;
        }

        int64_t volume() const {
            int64_t volume = this->max.x - this->min.x;
            volume        *= this->max.y - this->min.y;
            volume        *= this->max.z - this->min.z;
            return volume;
        }

    private:
        Vek max;
        Vek min;
};

std::pair<std::vector<Cube>, std::vector<bool>> read_data(std::string filename) {
    std::vector<Cube> cubes;
    std::vector<bool> states;

    std::ifstream file;
    file.open(filename);

    char c;

    while (file >> c) { //always o
        file >> c; // n or f
        states.push_back(c == 'n');
        if (c == 'f') {
            file >> c; // f
        }

        Vek a;
        Vek b;

        //      x    =    num    .    .    num    ,
        file >> c >> c >> a.x >> c >> c >> b.x >> c;
        file >> c >> c >> a.y >> c >> c >> b.y >> c;
        file >> c >> c >> a.z >> c >> c >> b.z;

        b.x++;
        b.y++;
        b.z++;

        cubes.push_back(Cube(a, b));
    }

    file.close();
    
    return make_pair(cubes, states);
}

std::pair<int64_t, int64_t> task(std::vector<Cube> cubes, std::vector<bool> states) {
    std::vector<Cube> activated;
    
    for (int i=0; i<cubes.size(); i++) {
        std::vector<Cube> next;
        for (int m=0; m < activated.size(); m++) {
            std::vector<Cube> temp = activated[m].minus(cubes[i]);
            next.insert(next.end(), temp.begin(), temp.end());
        }
        activated = next;

        if (states[i]) {
            activated.push_back(cubes[i]);
        }
    }

    Cube small(Vek{-50, -50, -50}, Vek{51, 51, 51});
    int64_t result1 = 0;
    int64_t result2 = 0;
    for (int m=0; m<activated.size(); m++) {
        result1 += (activated[m].intersection(small)).volume();
        result2 +=  activated[m].volume();
    }

    return std::make_pair(result1, result2);
}

int main() {
    auto p = read_data("input.txt");

    auto res = task(p.first, p.second);

    std::cout << "Task1: " << res.first << "\n"
              << "Task2: " << res.second << std::endl;

    return 0;
}
