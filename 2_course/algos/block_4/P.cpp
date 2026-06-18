#include <algorithm>
#include <iostream>
#include <queue>
#include <unordered_set>
#include <vector>

int find_max(std::vector<std::vector<int>>& map) {
  int max_fuel = 0;
  for (const auto& row : map) {
    auto it_max = std::max_element(row.begin(), row.end());
    max_fuel = std::max({*it_max, max_fuel});
  }

  return max_fuel;
}

bool can_fly_with_X_fuel(std::vector<std::vector<int>>& map, int X_fuel, int cities_count) {
  std::unordered_set<int> were_in_cities;
  std::queue<int> cities_to_discover;

  were_in_cities.insert(0);
  cities_to_discover.push(0);
  while (cities_to_discover.size() != 0) {
    int curr_city = cities_to_discover.front();
    cities_to_discover.pop();

    for (int next_city = 0; next_city < cities_count; next_city++) {
      if (map[curr_city][next_city] <= X_fuel) {
        if (!were_in_cities.contains(next_city)) {
          were_in_cities.insert(next_city);
          cities_to_discover.push(next_city);
        }
      }
    }
  }

  if (static_cast<int>(were_in_cities.size()) != cities_count) {
    return false;
  }

  were_in_cities.clear();

  were_in_cities.insert(0);
  cities_to_discover.push(0);
  while (cities_to_discover.size() != 0) {
    int curr_city = cities_to_discover.front();
    cities_to_discover.pop();

    for (int next_city = 0; next_city < cities_count; next_city++) {
      if (map[next_city][curr_city] <= X_fuel) {
        if (!were_in_cities.contains(next_city)) {
          were_in_cities.insert(next_city);
          cities_to_discover.push(next_city);
        }
      }
    }
  }

  if (static_cast<int>(were_in_cities.size()) != cities_count) {
    return false;
  }

  return true;
}

int main() {
  int cities_count;
  std::cin >> cities_count;

  std::vector<std::vector<int>> fuel_between_cities(cities_count, std::vector<int>(cities_count));
  for (int i = 0; i < cities_count; i++) {
    for (int j = 0; j < cities_count; j++) {
      int fuel_to_city;
      std::cin >> fuel_to_city;
      fuel_between_cities[i][j] = fuel_to_city;
    }
  }

  int left = 0;
  int right = find_max(fuel_between_cities);

  while (left < right) {
    int mid = (left + right) / 2;
    if (can_fly_with_X_fuel(fuel_between_cities, mid, cities_count)) {
      right = mid;
    } else {
      left = mid + 1;
    }
  }

  std::cout << left << std::endl;
}
