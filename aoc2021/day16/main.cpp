#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>

int64_t to_num(const std::vector<bool>& data, int start, int len) {
    int x = 0;

    for (int i=0; i < len; i++) {
        x = (x<<1) + data[i+start];
    }

    return x;
}

void print(const std::vector<bool>& data, int start, int len) {
    for (int i=0; i<len; i++) {
        std::cout << data[i+start];
    }
}

struct Package {
    Package(const std::vector<bool>& data, int start, int depth) : raw(0), subs() {
        this->version = to_num(data, start,   3);
        this->id      = to_num(data, start+3, 3);
        int current = start + 6;

        this->depth = depth;

        if (this->id == 4) {
            // read raw
            this->raw = 0;
            int x;
            do {
                x = to_num(data, current, 5);
                current += 5;
                this->raw = (this->raw << 4) + (x & 0xF);
            } while ((x & 0x10) != 0);
            this->bit_read = current - start;
        } else {
            if (not data[current]) {
                // search number of bits
                int num_bits = to_num(data, current+1, 15);
                current += 16;
                this->bit_read = num_bits + current - start;
                while (this->bit_read > current - start) {
                    Package sub = Package(data, current, depth+1);
                    current += sub.bit_read;
                    this->subs.push_back(sub);
                }
            } else {
                // search number of packages
                int num_packages = to_num(data, current+1, 11);
                current += 12;

                for (; num_packages > 0; num_packages--) {
                    Package sub = Package(data, current, depth+1);
                    current += sub.bit_read;
                    this->subs.push_back(sub);
                }

                this->bit_read = current - start;
            }
        }
    }

    Package(const std::vector<bool>& data) : Package(data, 0, 0) {}

    std::vector<Package> subs;
    int64_t raw;
    int version;
    int id;
    int bit_read;
    int depth;

    int task1() {
        int res = this->version;

        for (int i=0; i<this->subs.size(); i++) {
            res += subs[i].task1();
        }

        return res;
    }

    int64_t task2() {
        int64_t res;

        if (this->id == 0) {
            res = 0;
            for (int i=0; i<this->subs.size(); i++) {
                res += subs[i].task2();
            }
        } else if (this->id == 1) {
            res = 1;
            for (int i=0; i<this->subs.size(); i++) {
                res *= subs[i].task2();
            }
        } else if (this->id == 2) {
            res = this->subs[0].task2();
            for (int i=1; i<this->subs.size(); i++) {
                res = std::min(res, subs[i].task2());
            }
        } else if (this->id == 3) {
            res = this->subs[0].task2();
            for (int i=1; i<this->subs.size(); i++) {
                res = std::max(res, subs[i].task2());
            }
        } else if (this->id == 4) {
            res = this->raw;
        } else if (this->id == 5) {
            res = this->subs[0].task2() > this->subs[1].task2();
        } else if (this->id == 6) {
            res = this->subs[0].task2() < this->subs[1].task2();
        } else if (this->id == 7) {
            res = this->subs[0].task2() == this->subs[1].task2();
        }

        return res;
    }
};

std::ostream& operator<<(std::ostream& os, const Package& p) {
    for (int i=0; i<p.depth; i++) {
        std::cout << "\t";
    }
    os << "V: " << p.version << ", T: " << p.id
       << " (" << p.raw << ")" << std::endl;
    for (int i=0; i<p.subs.size(); i++) {
        os << p.subs[i];
    }
    return os;
}

std::vector<bool> read_data(std::string filename) {
    std::ifstream file;
    file.open(filename);
    
    std::string line;
    file >> line;

    file.close();

    std::vector<bool> result;
    char x;
    for (int i=0; i<line.size(); i++) {
        if (line[i] >= 'A') {
            x = line[i] - 'A' + 10;
        }
        else {
            x = line[i] - '0';
        }
        result.push_back(x & 0b1000);
        result.push_back(x & 0b0100);
        result.push_back(x & 0b0010);
        result.push_back(x & 0b0001);
    }

    return result;
}

int main() {
    const std::vector<bool> data = read_data("input.txt");
    Package pack(data);

    int res1 = pack.task1();
    int64_t res2 = pack.task2();

    std::cout << "Task1: " << res1 << "\n"
              << "Task2: " << res2 << std::endl;

    return 0;
}
