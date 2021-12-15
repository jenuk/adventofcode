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

        std::vector<Position> get_neighbors(Position p) const;

        T distance(const Position& s, const Position& t) const;

        void set(const T& val, const Position& p);
        T operator[](Position p) const;

        void set_virtual_dim(int f_n, int f_m);

        Position topleft() const;
        Position bottomright() const;

        friend std::istream& operator>>(std::istream& is, Grid<int>& grid);

        template <class S>
        friend class Grid;

    private:
        Grid<bool> get_empty_mask() const;
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
std::vector<Position> Grid<T>::get_neighbors(Position p) const {
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
    typedef std::tuple<T, T, Position> Q_El;
    auto cmp = [](Q_El left, Q_El right) { return std::get<0>(left) > std::get<0>(right); };
    std::priority_queue<Q_El, std::vector<Q_El>, decltype(cmp)> q(cmp);

    Grid<bool> visited = this->get_empty_mask();

    q.push(std::make_tuple(0, 0, s));

    T dist, next_dist, next_adist;
    Position current;

    while (q.size() > 0) {
        Q_El top = q.top();
        q.pop();

        dist    = std::get<1>(top);
        current = std::get<2>(top);

        if (current == t) {
            return dist;
        }
        if (visited[current]) {
            continue;
        }

        visited.set(true, current);
        std::vector<Position> neighbors = this->get_neighbors(current);
        for (int i=0; i<neighbors.size(); i++) {
            next_dist  = dist + (*this)[neighbors[i]];
            next_adist = next_dist + min_distance(neighbors[i], t);
            q.push(std::make_tuple(next_adist, next_dist, neighbors[i]));
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

    return (this->_data[p.x][p.y] + d - 1)%9 + 1;
}
template <class T>
void Grid<T>::set(const T& val, const Position& p) {
    this->_data[p.x][p.y] = val;
}

template <class T>
Grid<bool> Grid<T>::get_empty_mask() const {
    Grid<bool> res;

    for (int i=0; i<this->_n; i++) {
        res._data.push_back({});
        for (int j=0; j<this->_m; j++) {
            res._data[i].push_back(false);
        }
    }

    return res;
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
    int res2 = grid.distance(grid.topleft(), grid.bottomright());

    std::cout << res1 << "\n";
    std::cout << res2 << std::endl;

    return 0;
}
