#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Point {
    int x, y;
};

vector<Point> points;
double cx, cy;

int get_quadrant(double x, double y) {
    if (y >= 0 && x > 0) return 0;
    if (y > 0 && x <= 0) return 1;
    if (y <= 0 && x < 0) return 2;
    return 3;
}

bool compare(int a, int b) {
    double ax = points[a].x - cx;
    double ay = points[a].y - cy;
    double bx = points[b].x - cx;
    double by = points[b].y - cy;

    int qa = get_quadrant(ax, ay);
    int qb = get_quadrant(bx, by);
    if (qa != qb) {
        return qa < qb;
    }

    double mul = ax * by - ay * bx;
    if (mul != 0) {
        return mul > 0;
    }

    double dist_a = ax * ax + ay * ay;
    double dist_b = bx * bx + by * by;

    return dist_a < dist_b;
}

int main() {
    int N;
    cin >> N;

    points.resize(N + 1);
    
    long long sum_x = 0, sum_y = 0;
    for (int i = 1; i <= N; i++) {
        cin >> points[i].x >> points[i].y;
        sum_x += points[i].x;
        sum_y += points[i].y;
    }

    cx = (double)(sum_x) / N;
    cy = (double)(sum_y) / N;

    vector<int> order(N);
    for (int i = 0; i < N; i++) {
        order[i] = i + 1;
    }

    sort(order.begin(), order.end(), compare);

    int start = 0;
    for (int i = 0; i < N; i++) {
        if (order[i] == 1) {
            start = i;
            break;
        }
    }

    cout << N << "\n";
    for (int i = 0; i < N; i++) {
        int idx = (start + i) % N;
        cout << order[idx] << "\n";
    }
}
