#include <iostream>
#include <vector>
#include <random>

int partition(std::vector<int>& arr, int left, int right, int pivot_index) {
    int pivot_value = arr[pivot_index];
    std::swap(arr[pivot_index], arr[right]);
    
    int store_index = left;
    for (int i = left; i < right; i++) {
        if (arr[i] < pivot_value) {
            std::swap(arr[i], arr[store_index]);
            store_index++;
        }
    }
    std::swap(arr[store_index], arr[right]);
    return store_index;
}

int median_of_medians(std::vector<int>& arr, int left, int right, int k) {
    if (right - left + 1 <= 5) {
        std::sort(arr.begin() + left, arr.begin() + right + 1);
        return arr[left + k];
    }
    
    int num_groups = (right - left + 1) / 5;
    std::vector<int> medians;
    medians.reserve(num_groups);
    
    for (int i = 0; i < num_groups; i++) {
        int group_left = left + i * 5;
        int group_right = group_left + 4;
        std::sort(arr.begin() + group_left, arr.begin() + group_right + 1);
        medians.push_back(arr[group_left + 2]);
    }
    
    int pivot = median_of_medians(medians, 0, medians.size() - 1, medians.size() / 2);
    
    int pivot_index = left;
    while (pivot_index <= right && arr[pivot_index] != pivot) {
        pivot_index++;
    }
    
    int final_pivot_index = partition(arr, left, right, pivot_index);
    int rank = final_pivot_index - left;
    
    if (rank == k) {
        return arr[final_pivot_index];
    } else if (k < rank) {
        return median_of_medians(arr, left, final_pivot_index - 1, k);
    } else {
        return median_of_medians(arr, final_pivot_index + 1, right, k - rank - 1);
    }
}

double find_median(std::vector<int> arr) {
    int n = arr.size();
    if (n == 0) {
        return 0.0;
    } else if (n % 2 == 1) {
        return median_of_medians(arr, 0, n - 1, n / 2);
    } else {
        int mid_right = median_of_medians(arr, 0, n - 1, n / 2);
        int mid_left = median_of_medians(arr, 0, n - 1, n / 2 - 1);
        return (mid_left + mid_right) / 2.0;
    }
}

int main() {
    std::vector<int> test(10001);
    std::iota(test.begin(), test.end(), 0);
    std::mt19937 gen{ std::random_device{}() };
    std::shuffle(test.begin(), test.end(), gen);

    std::cout << find_median({7, 2, 9, 1, 5, 3, 8}) << std::endl;   // 5
    std::cout << find_median({7, 2, 9, 1, 5, 3}) << std::endl;      // 4
    std::cout << find_median({1, 1, 1, 1, 1}) << std::endl;         // 1
    std::cout << find_median({7, 2, 9, 1}) << std::endl;            // 4.5
    std::cout << find_median({7, 2, 9}) << std::endl;               // 7
    std::cout << find_median(test) << std::endl;                    // 5000
    std::cout << find_median({}) << std::endl;                      // 0
}
