#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

long long sum_by_dir(vector<long long> vector_dir) {
    sort(vector_dir.begin(), vector_dir.end());
    long long impact = 0, prefix_sum = 0;

    for (int i = 0; i < (int)vector_dir.size(); i++) {
        impact += vector_dir[i] * i - prefix_sum;
        prefix_sum += vector_dir[i];
    }

    return 2LL * impact;
}

int main() {
    int houses_count;
    cin >> houses_count;

    vector <long long> dist_x(houses_count), dist_y(houses_count);
    for (int i = 0; i < houses_count; i++) {
        cin >> dist_x[i] >> dist_y[i];
    }

    long long sum_x = sum_by_dir(dist_x);
    long long sum_y = sum_by_dir(dist_y);
    long long total_sum = sum_x + sum_y;

    cout << total_sum / (1LL * houses_count * (houses_count - 1));
}
