#include <iostream>
#include <unordered_set>
#include <vector>

int main() {
  int piggy_banks_count;
  std::cin >> piggy_banks_count;

  std::vector<int> keys(piggy_banks_count + 1);
  for (int i = 1; i < piggy_banks_count + 1; i++) {
    int key_from_piggy_i_in_here;
    std::cin >> key_from_piggy_i_in_here;
    keys[i] = key_from_piggy_i_in_here;
  }

  int cycles = 0;
  std::unordered_set<int> all_discovered_piggy_banks;

  for (int i = 1; i < piggy_banks_count + 1; i++) {
    int curr = i;
    std::unordered_set<int> currently_visited_piggy_banks;

    if (all_discovered_piggy_banks.contains(i)) {
      continue;
    }

    while (!all_discovered_piggy_banks.contains(curr)) {
      all_discovered_piggy_banks.insert(curr);
      currently_visited_piggy_banks.insert(curr);
      curr = keys[curr];
    }

    if (currently_visited_piggy_banks.contains(curr)) {
      cycles++;
    }
  }

  std::cout << cycles << std::endl;
}
