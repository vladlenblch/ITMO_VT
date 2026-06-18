#include <iostream>
#include <vector>
#include <algorithm>

double find_median(std::vector<int> arr) {
    size_t n = arr.size();

    std::nth_element(arr.begin(), arr.begin() + n / 2, arr.end());
    double mid = arr[n / 2];

    if (n % 2 == 1) {
        return mid;
    } else {
        std::nth_element(arr.begin(), arr.begin() + n / 2 - 1, arr.begin() + n / 2);
        double mid_left = arr[n / 2 - 1];
        return (mid + mid_left) / 2.0;
    }
}

int main() {
    std::vector<int> arr = {7, 2, 9, 1, 5, 3, 8};

    std::cout << "Median: " << find_median(arr) << std::endl;
}
