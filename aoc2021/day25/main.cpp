#include <iostream>
#include <fstream>
#include <vector>
#include <utility>

enum Cucubmber {
    EMPTY,
    WEST,
    SOUTH,
};

struct Position {
    int x;
    int y;
};

class OceanFloor {
    public:
        OceanFloor(int n, int m) {
            for (int i=0; i<n; i++) {
                this->field.push_back(std::vector<Cucubmber>(m, EMPTY));
            }
        }

        OceanFloor(std::string filename) {
            std::ifstream file;
            file.open(filename);

            std::string line;
            int i = 0;
            while (std::getline(file, line)) {
                this->field.push_back(std::vector<Cucubmber>(line.size(), EMPTY));
                for (int j=0; j<line.size(); j++) {
                    if (line[j] == '>') {
                        this->field[i][j] = WEST;
                    } else if (line[j] == 'v') {
                        this->field[i][j] = SOUTH;
                    }
                }
                i++;
            }
        };

        Cucubmber operator[](Position p) const {
            while (p.x >= this->field.size()) {
                p.x -= this->field.size();
            }
            while (p.y >= this->field[p.x].size()) {
                p.y -= this->field[p.x].size();
            }
            return this->field[p.x][p.y];
        };

        Cucubmber& operator[](Position p) {
            while (p.x >= this->field.size()) {
                p.x -= this->field.size();
            }
            while (p.y >= this->field[p.x].size()) {
                p.y -= this->field[p.x].size();
            }
            return this->field[p.x][p.y];
        };

        bool operator==(const OceanFloor& other) const {
            if (other.field.size() != this->field.size()) {
                return false;
            }

            for (int i=0; i<other.field.size(); i++) {
                if (other.field[i].size() != this->field[i].size()) {
                    return false;
                }

                for (int j=0; j<other.field[i].size(); j++) {
                    if (other.field[i][j] != this->field[i][j]) {
                        return false;
                    }
                }
            }

            return true;
        }
        bool operator!=(const OceanFloor& other) const {
            return not ((*this) == other);
        }

        std::pair<OceanFloor, bool> next() {
            OceanFloor next(this->field.size(), this->field[0].size());
            bool changed = false;

            //move west
            for (int i=0; i<this->field.size(); i++) {
                for (int j=0; j<this->field[i].size(); j++) {
                    if ((*this)[Position{i, j}] == WEST) {
                        if ((*this)[Position{i, j+1}] == EMPTY) {
                            changed = true;
                            next[Position{i, j+1}] = WEST;
                            j++;
                        } else {
                            next[Position{i, j}] = WEST;
                        }
                    }
                }
            }

            //move south
            for (int j=0; j<this->field[0].size(); j++) {
                for (int i=0; i<this->field.size(); i++) {
                    if ((*this)[Position{i, j}] == SOUTH) {
                        if (((*this)[Position{i+1, j}] == EMPTY
                            or (*this)[Position{i+1, j}] == WEST)
                            and next[Position{i+1, j}] == EMPTY) {
                            changed = true;
                            next[Position{i+1, j}] = SOUTH;
                            i++;
                        } else {
                            next[Position{i, j}] = SOUTH;
                        }
                    }
                }
            }

            return std::make_pair(next, changed);
        }


        friend std::ostream& operator<<(std::ostream& os, const OceanFloor& floor);

    private:
        std::vector<std::vector<Cucubmber>> field;
};

std::ostream& operator<<(std::ostream& os, const OceanFloor& floor) {
    for (int i=0; i<floor.field.size(); i++) {
        for (int j=0; j<floor.field[i].size(); j++) {
            if (floor[Position{i,j}] == EMPTY) {
                os << ".";
            } else if (floor[Position{i,j}] == WEST) {
                os << ">";
            } else if (floor[Position{i,j}] == SOUTH) {
                os << "v";
            }
        }
        os << "\n";
    }
    return os;
}


int main() {
    OceanFloor floor("input.txt");
    int counter = 0;
    bool progress; 
    do {
        auto p   = floor.next();
        floor    = p.first;
        progress = p.second;
        counter++;
    } while (progress);

    std::cout << counter << std::endl;

    return 0;
}
