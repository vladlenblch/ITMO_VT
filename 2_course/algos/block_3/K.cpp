#include <iostream>
#include <set>
#include <vector>

int main() {
  long long memory_cells_count, requests_count;
  std::cin >> memory_cells_count >> requests_count;

  std::set<std::pair<long long, long long>> left_right;
  std::set<std::pair<long long, long long>> len_left;
  std::vector<std::pair<long long, long long>> blocks(requests_count + 1, {-1, -1});

  left_right.insert({1, memory_cells_count});
  len_left.insert({memory_cells_count, 1});

  for (long long request_index = 1; request_index <= requests_count; request_index++) {
    int request;
    std::cin >> request;

    if (request > 0) {
      auto it = len_left.lower_bound({request, 0});
      if (it == len_left.end()) {
        std::cout << -1 << std::endl;
        continue;
      }

      long long len = it->first;
      long long left = it->second;
      long long right = left + len - 1;
      long long block_right = left + request - 1;

      blocks[request_index] = {left, block_right};

      std::cout << left << std::endl;

      len_left.erase(it);
      left_right.erase({left, right});

      if (block_right < right) {
        long long new_left = block_right + 1;
        left_right.insert({new_left, right});
        len_left.insert({right - new_left + 1, new_left});
      }

      continue;
    }

    long long block_return_index = -request;
    if (blocks[block_return_index].first == -1) {
      continue;
    }

    long long left = blocks[block_return_index].first;
    long long right = blocks[block_return_index].second;
    long long new_left = left;
    long long new_right = right;

    auto it = left_right.lower_bound({left, 0});
    if (it != left_right.end() && it->first == right + 1) {
      new_right = it->second;

      len_left.erase({it->second - it->first + 1, it->first});
      left_right.erase(it);
    }

    it = left_right.lower_bound({left, 0});
    if (it != left_right.begin()) {
      auto prev_it = std::prev(it);
      if (prev_it->second == left - 1) {
        new_left = prev_it->first;

        len_left.erase({prev_it->second - prev_it->first + 1, prev_it->first});
        left_right.erase(prev_it);
      }
    }

    left_right.insert({new_left, new_right});
    len_left.insert({new_right - new_left + 1, new_left});
    blocks[block_return_index] = {-1, -1};
  }
}
