#include <iostream>
#include <fstream>
#include <utility>
#include <vector>

class Number {
    public:
        Number() : left(nullptr), right(nullptr), val(0), is_regular(true) {}
        Number(Number* a, Number* b) : left(a), right(b), val(0), is_regular(false) {}
        Number(int val) : left(nullptr), right(nullptr), val(val), is_regular(true) {}

        Number(const Number& num) {
            this->is_regular = num.is_regular;
            this->val = num.val;
            this->left = nullptr;
            this->right = nullptr;
            if (not this->is_regular) {
                this->left = new Number(*num.left);
                this->right = new Number(*num.right);
            }
        }

        Number& operator=(const Number& num) {
            if (not this->is_regular) {
                delete this->left;
                delete this->right;
            }
            this->is_regular = num.is_regular;
            this->val = num.val;
            this->left = nullptr;
            this->right = nullptr;
            if (not this->is_regular) {
                this->left = new Number(*num.left);
                this->right = new Number(*num.right);
            }

            return *this;
        }

        ~Number() {
            delete this->left;
            delete this->right;
        }

        void reduce() {
            while (true) {
                auto p = this->explode(0);
                if (p.first) {
                    continue;
                }
                if (this->split()) {
                    continue;
                }
                break;
            }
        }
        std::pair<bool, std::pair<int, int>> explode(int depth) {
            if (this->is_regular) {
                return std::make_pair(false, std::make_pair(0, 0));
            }
            if (depth == 4) {
                std::pair<int, int> a = std::make_pair(this->left->val,
                                                       this->right->val);
                delete this->left;
                delete this->right;
                this->is_regular = true;
                this->val = 0;
                return std::make_pair(true, a);
            }
            else {
                auto p = this->left->explode(depth+1);
                if (p.first) {
                    if (p.second.second != 0) {
                        this->right->add_left(p.second.second);
                    }
                    p.second.second = 0;
                    return p;
                } else {
                    p = this->right->explode(depth+1);
                    if (not p.first) {
                        return std::make_pair(false, std::make_pair(0, 0));
                    }
                    if (p.second.first != 0) {
                        this->left->add_right(p.second.first);
                    }
                    p.second.first = 0;
                    return p;
                }
            }
        }
        bool split() {
            if (this->is_regular) {
                if (this->val > 9) {
                    this->is_regular = false;
                    this->left = new Number(this->val/2);
                    this->right = new Number(this->val/2 + (this->val%2));
                    return true;
                }
                return false;
            } else {
                if (this->left->split()) {
                    return true;
                } else {
                    return this->right->split();
                }
            }
        }
        void add_left(int x) {
            if (this->is_regular) {
                this->val += x;
            } else {
                this->left->add_left(x);
            }
        }
        void add_right(int x) {
            if (this->is_regular) {
                this->val += x;
            } else {
                this->right->add_right(x);
            }
        }

        int magnitude() const {
            if (this->is_regular) {
                return this->val;
            } else {
                return 3*this->left->magnitude() + 2*this->right->magnitude();
            }
        }

        Number& operator+(const Number& other) const {
            Number* res = new Number(new Number(*this), new Number(other));
            res->reduce();
            return *res;
        }

        Number& operator+=(const Number& other) {
            // some error is introduced in this function
            // don't know where

            // shallow copy this
            Number* cp     = new Number;
            cp->is_regular = this->is_regular;
            cp->val        = this->val;
            cp->left       = this->left;
            cp->right      = this->right;

            this->left  = cp;
            this->right = new Number(other);

            this->reduce();

            return *this;
        }
        
        friend std::ostream& operator<<(std::ostream& os, const Number& num);
        friend std::istream& operator>>(std::istream& is, Number& num);

    private:
        bool is_regular;
        Number* left;
        Number* right;
        int val;
};


std::ostream& operator<<(std::ostream& os, const Number& num) {
    if (num.is_regular) {
        os << num.val;
    } else {
        os << "[" << (*num.left) << "," << (*num.right) << "]";
    }
    return os;
}

std::istream& operator>>(std::istream& is, Number& num) {
    if (num.left != nullptr) {
        delete num.left;
        delete num.right;
        num.left = nullptr;
        num.right = nullptr;
    }

    char c;
    is >> c;
    if (c == '[') {
        Number* a = new Number();
        Number* b = new Number();
        is >> (*a) >> c >> (*b) >> c;
        num.left = a;
        num.right = b;
        num.is_regular = false;
        num.val = 0;
    } else {
        num.is_regular = true;
        is.putback(c);
        is >> num.val;
    }
    return is;
}

int main() {
    std::vector<Number> nums;
    Number num;

    std::ifstream file;
    file.open("input.txt");

    while (file >> num) {
        nums.push_back(num);
    }

    file.close();

    Number num_task1(nums[0]);
    for (int i=1; i<nums.size(); i++) {
        num_task1 = num_task1 + nums[i];
    }
    int res1 = num_task1.magnitude();

    int res2 = 0;
    for (int i=0; i<nums.size(); i++) {
        for (int j=0; j<nums.size(); j++) {
            res2 = std::max((nums[i] + nums[j]).magnitude(), res2);
        }
    }
    
    std::cout << "Task1: " << res1 << "\n"
              << "Task2: " << res2 << std::endl;

    return 0;
}
