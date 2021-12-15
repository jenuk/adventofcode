#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <queue>
#include <tuple>

struct Position{
    int x;
    int y;

    bool operator==(const Position& other) const {
        return (this->x == other.x) and (this->y == other.y);
    }
};


int min_distance(const Position& a, const Position& b) {
    return std::abs(a.x - b.x) + std::abs(a.y - b.y);
}


template <class T>
class Grid {
    public:
        Grid();
        Grid(int f_n, int f_m);

        std::vector<Position> get_neighbors(const Position& p) const;

        T distance(const Position& s, const Position& t) const;
        T distance(const Position& s, const Position& t, const bool verbose) const;

        void set(const T& val, const Position& p);
        T operator[](Position p) const;

        void set_virtual_dim(int f_n, int f_m);

        Position topleft() const;
        Position bottomright() const;

        Grid operator+(const Grid& other) const;
        void write(std::string filename) const;

        friend std::istream& operator>>(std::istream& is, Grid<int>& grid);

        template <class S>
        friend class Grid;

    private:
        template <class S>
        Grid<S> get_empty_mask() const;
        std::vector<std::vector<T>> _data;
        int _n;
        int _m;
        int f_n;
        int f_m;
};


template <class T>
Grid<T>::Grid() : f_n(1), f_m(1) {}

template <class T>
Grid<T>::Grid(int f_n, int f_m) : f_n(f_n), f_m(f_m) {}


template <class T>
std::vector<Position> Grid<T>::get_neighbors(const Position& p) const {
    std::vector<Position> res;

    if (p.x > 0) {
        res.push_back(Position{p.x-1, p.y});
    }
    if (p.y > 0) {
        res.push_back(Position{p.x, p.y-1});
    }
    if (p.x+1 < this->_n) {
        res.push_back(Position{p.x+1, p.y});
    }
    if (p.y+1 < this->_m) {
        res.push_back(Position{p.x, p.y+1});
    }

    return res;
}

template <class T>
T Grid<T>::distance(const Position& s, const Position& t) const {
    return this->distance(s, t, false);
}

template <class T>
T Grid<T>::distance(const Position& s, const Position& t, const bool verbose) const {
    typedef std::tuple<T, T, Position> Q_El;
    auto cmp = [](Q_El left, Q_El right) { return std::get<0>(left) > std::get<0>(right); };
    std::priority_queue<Q_El, std::vector<Q_El>, decltype(cmp)> q_forward(cmp);
    std::priority_queue<Q_El, std::vector<Q_El>, decltype(cmp)> q_backward(cmp);

    Grid<bool> visited_forward   = this->get_empty_mask<bool>();
    Grid<int> distances_forward  = this->get_empty_mask<int>();

    Grid<bool> visited_backward  = this->get_empty_mask<bool>();
    Grid<int> distances_backward = this->get_empty_mask<int>();

    q_forward.push(std::make_tuple(0, 0, s));
    q_backward.push(std::make_tuple(0, 0, t));

    T dist, next_dist, next_adist;
    Position current;
    int num_step = 0;
    int freq = 500;

    auto step = [&](std::priority_queue<Q_El, std::vector<Q_El>, decltype(cmp)>& q,
                   Grid<bool>& visited, Grid<int>& distances, bool forward) {
        Q_El top = q.top();
        q.pop();

        dist    = std::get<1>(top);
        current = std::get<2>(top);

        if (visited[current]) {
            return;
        }
        num_step++;

        visited.set(true, current);
        distances.set(dist, current);

        std::vector<Position> neighbors = this->get_neighbors(current);
        for (int i=0; i<neighbors.size(); i++) {
            if (forward) {
                next_dist  = dist + ((*this)[neighbors[i]]-1)%9 + 1;
                next_adist = next_dist + min_distance(neighbors[i], t);
            } else {
                next_dist  = dist + ((*this)[current]-1)%9 + 1;
                next_adist = next_dist + min_distance(neighbors[i], s);
            }
            q.push(std::make_tuple(next_adist, next_dist, neighbors[i]));
        }

        return;
    };

    while (q_forward.size() > 0 or q_backward.size() > 0) {
        if (q_forward.size() > 0) {
            step(q_forward, visited_forward, distances_forward, true);
            if (visited_forward[current] and visited_backward[current]) {
                if (verbose) {
                    (distances_forward + distances_backward).write("out/end");
                }
                return distances_forward[current] + distances_backward[current];
            }
            if (verbose and num_step%freq == 0) {
                (visited_forward + visited_backward).write("out/" + std::to_string(num_step/freq));
                num_step++;
            }
        }

        if (q_backward.size() > 0) {
            step(q_backward, visited_backward, distances_backward, false);
            if (visited_forward[current] and visited_backward[current]) {
                if (verbose) {
                    (distances_forward + distances_backward).write("out/end");
                }
                return distances_forward[current] + distances_backward[current];
            }
            if (verbose and num_step%freq == 0) {
                (visited_forward + visited_backward).write("out/" + std::to_string(num_step/freq));
                num_step++;
            }
        }

    }

    // t not found
    return 0;
}

template <class T>
void Grid<T>::set_virtual_dim(int f_n, int f_m) {
    this->_n = f_n * this->_data.size();
    this->f_n = f_n;

    this->_m = f_m * this->_data[0].size();
    this->f_m = f_m;
}

template <class T>
Position Grid<T>::topleft() const {
    return Position{0, 0};
}
template <class T>
Position Grid<T>::bottomright() const {
    return Position{this->_n-1, this->_m-1};
}

template <class T>
T Grid<T>::operator[](Position p) const {
    int d = 0;
    while (p.x >= this->_data.size()) {
        p.x -= this->_data.size();
        d++;
    }

    while (p.y >= this->_data.size()) {
        p.y -= this->_data[0].size();
        d++;
    }

    return this->_data[p.x][p.y] + d;
}
template <class T>
void Grid<T>::set(const T& val, const Position& p) {
    this->_data[p.x][p.y] = val;
}

template <class T>
template <class S>
Grid<S> Grid<T>::get_empty_mask() const {
    Grid<S> res;

    for (int i=0; i<this->_n; i++) {
        res._data.push_back({});
        for (int j=0; j<this->_m; j++) {
            res._data[i].push_back(S());
        }
    }

    res._n = this->_n;
    res._m = this->_m;

    return res;
}


template <class T>
Grid<T> Grid<T>::operator+(const Grid<T>& other) const {
    // assert(this->_n == other._n and this->_m == other._m);

    Grid<T> result;
    result._n = this->_n;
    result._m = this->_m;

    Position p;
    for (int i=0; i<this->_n; i++){
        result._data.push_back({});
        for (int j=0; j<this->_m; j++) {
            p = Position{i, j};
            result._data[i].push_back((*this)[p] + other[p]);
        }
    }

    return result;
}

template <class T>
std::ostream& operator<<(std::ostream& os, const Grid<T>& grid);

template <>
void Grid<int>::write(std::string filename) const {
    std::ofstream file;
    file.open(filename+".pgm");

    file << "P2\n";
    file << this->_n << " " << this->_m << "\n";
    file << 3000 << "\n";

    file << (*this);

    file << std::flush;

    file.close();
}

template <>
void Grid<bool>::write(std::string filename) const {
    std::ofstream file;
    file.open(filename+".pbm");

    file << "P1\n";
    file << this->_n << " " << this->_m << "\n";

    file << (*this);

    file << std::flush;

    file.close();
}


template <class T>
std::ostream& operator<<(std::ostream& os, const Grid<T>& grid) {
    Position end = grid.bottomright();
    for (int i=0; i<=end.x; i++) {
        for (int j=0; j<=end.y; j++) {
            os << grid[Position{i, j}] << " ";
        }
        os << "\n";
    }

    return os;
}


std::istream& operator>>(std::istream& is, Grid<int>& grid) {
    grid._data.clear();

    std::string line;

    while (is >> line) {
        std::vector<int> vec;
        for (int k=0; k<line.size(); k++) {
            vec.push_back(line[k] - '0');
        }
        grid._data.push_back(vec);
    }

    grid._n = grid.f_n * grid._data.size();
    grid._m = grid.f_m * grid._data[0].size();

    return is;
}


int main() {
    std::ifstream file;
    file.open("input.txt");

    Grid<int> grid;
    file >> grid;

    file.close();

    int res1 = grid.distance(grid.topleft(), grid.bottomright());
    grid.set_virtual_dim(5, 5);
    int res2 = grid.distance(grid.topleft(), grid.bottomright(), true);

    std::cout << res1 << "\n";
    std::cout << res2 << std::endl;

    return 0;
}
