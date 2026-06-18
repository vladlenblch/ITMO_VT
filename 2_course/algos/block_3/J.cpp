#include <deque>
#include <iostream>

void balance_deques(std::deque<int>& left_queue, std::deque<int>& right_queue) {
  int goblin_relocant = right_queue.front();
  right_queue.pop_front();
  left_queue.push_back(goblin_relocant);
}

int main() {
  int request_count = 0;
  std::cin >> request_count;

  std::deque<int> left_queue;
  std::deque<int> right_queue;
  for (int i = 0; i < request_count; i++) {
    char request;
    std::cin >> request;

    int goblin_id = 0;
    if (request == '-') {
      int welcome = left_queue.front();
      left_queue.pop_front();
      std::cout << welcome << std::endl;

      if (left_queue.size() < right_queue.size()) {
        balance_deques(left_queue, right_queue);
      }

      continue;
    }

    std::cin >> goblin_id;
    if (request == '+') {
      right_queue.push_back(goblin_id);
      if (left_queue.size() < right_queue.size()) {
        balance_deques(left_queue, right_queue);
      }

      continue;
    }

    if (request == '*') {
      right_queue.push_front(goblin_id);
      if (left_queue.size() < right_queue.size()) {
        balance_deques(left_queue, right_queue);
      }

      continue;
    }
  }
}
