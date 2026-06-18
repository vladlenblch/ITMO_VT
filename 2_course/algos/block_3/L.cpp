#include <deque>
#include <iostream>

int main() {
  int len, window_size;
  std::cin >> len >> window_size;

  std::deque<std::pair<int, int>> window;
  for (int i = 0; i < len; i++) {
    int curr_elem;
    std::cin >> curr_elem;

    while (window.size() != 0 && window.back().first >= curr_elem) {
      window.pop_back();
    }

    window.push_back({curr_elem, i});

    while (window.size() != 0 && window.front().second <= i - window_size) {
      window.pop_front();
    }

    if (i >= window_size - 1) {
      std::cout << window.front().first << " ";
    }
  }
}