#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <utility>

struct Position {
    int x;
    int y;
};

class Image {
    public:
        Image(std::vector<bool> map, bool pad) : map(map), pad(pad) {}
        Image(std::string filename) : map(512), pad(false) {
            std::ifstream file;
            file.open(filename);

            std::string line;
            std::getline(file, line);

            for (int i=0; i<line.size(); i++) {
                map[i] = (line[i] == '#');
            }

            std::getline(file, line); // empty line

            while (std::getline(file, line)) {
                std::vector<bool> row(line.size());
                for (int i=0; i<line.size(); i++) {
                    row[i] = (line[i] == '#');
                }
                this->image.push_back(row);

            }

            file.close();
        }

        bool operator[](Position p) const {
            if (p.x < 0 or p.x >= this->image.size()
                    or p.y < 0 or p.y >= this->image[p.x].size()) {
                return this->pad;
            } else {
                return this->image[p.x][p.y];
            }

        }

        bool kernel(int i, int j) const {
            int num = 0;
            for (int x=i-1; x<=i+1; x++) {
                for (int y=j-1; y<=j+1; y++) {
                    num = (num << 1) + (*this)[Position{x, y}];
                }
            }
            return this->map[num];
        }

        Image enhance() const {
            Image next(this->map, this->kernel(-3, -3));
            int extra = 1;
            for (int i=0; i<this->image.size()+2*extra; i++) {
                std::vector<bool> row(image[0].size()+2*extra);
                for (int j=0; j<this->image[0].size()+2*extra; j++) {
                    row[j] = this->kernel(i-extra, j-extra);
                }
                next.image.push_back(row);
            }
            return next;
        }

        int sum() const {
            int res = 0;
            for (int i=0; i<image.size(); i++) {
                for (int j=0; j<image[i].size(); j++) {
                    res += this->image[i][j];
                }
            }
            return res;
        }

        std::pair<int, int> get_dimension() const {
            return std::make_pair(this->image.size(), this->image[0].size());
        }

    private:
        bool pad;
        std::vector<bool> map;
        std::vector<std::vector<bool>> image;
};

std::ostream& operator<<(std::ostream& os, const Image& img) {
    std::pair<int, int> p = img.get_dimension();

    for (int i=-1; i<=p.first; i++) {
        for (int j=-1; j<=p.second; j++) {
            os << (img[Position{i, j}] ? '#' : '.');
        }
        os << "\n";
    }

    return os;
}

int main() {
    Image img("input.txt");

    int res1 = 0;
    int res2 = 0;

    for (int i=1; i<=50; i++) {
        img = img.enhance();
        if (i == 2) {
            res1 = img.sum();
        }
    }
    res2 = img.sum();

    std::cout << "Task1: " << res1
              << "\nTask2: " << res2 << std::endl;
}
