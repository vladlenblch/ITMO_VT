#include <iostream>
#include <set>
#include <vector>

int main() {
  int cars_count, queue_length;
  size_t max_cars_on_floor;
  std::cin >> cars_count >> max_cars_on_floor >> queue_length;

  std::vector<int> cars_queue(queue_length);

  for (int i = 0; i < queue_length; i++) {
    std::cin >> cars_queue[i];
  }

  std::vector<int> next_pos(queue_length);
  std::vector<int> last_pos(cars_count + 1, 1000000000);

  for (int i = queue_length - 1; i >= 0; i--) {
    next_pos[i] = last_pos[cars_queue[i]];
    last_pos[cars_queue[i]] = i;
  }

  int mom_call_count = 0;
  std::set<int> cars_on_floor;
  std::set<std::pair<int, int>> future_cars;
  std::vector<int> next_use_on_floor(cars_count + 1, -1);

  for (int car_index = 0; car_index < queue_length; car_index++) {
    int curr_car = cars_queue[car_index];

    if (cars_on_floor.contains(curr_car)) {
      future_cars.erase({next_use_on_floor[curr_car], curr_car});
      next_use_on_floor[curr_car] = next_pos[car_index];
      future_cars.insert({next_use_on_floor[curr_car], curr_car});
      continue;
    }

    mom_call_count++;

    if (cars_on_floor.size() == max_cars_on_floor) {
      auto it = std::prev(future_cars.end());
      int car_to_remove = it->second;
      cars_on_floor.erase(car_to_remove);
      future_cars.erase(it);
    }

    cars_on_floor.insert(curr_car);
    next_use_on_floor[curr_car] = next_pos[car_index];
    future_cars.insert({next_use_on_floor[curr_car], curr_car});
  }

  std::cout << mom_call_count << std::endl;
}
