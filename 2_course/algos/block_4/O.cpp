#include <iostream>
#include <queue>
#include <vector>

int main() {
  int students_count, pairs_count;
  std::cin >> students_count >> pairs_count;

  std::vector<std::vector<int>> students(students_count);
  for (int i = 0; i < pairs_count; i++) {
    int dummy_1, dummy_2;
    std::cin >> dummy_1 >> dummy_2;

    dummy_1--;
    dummy_2--;

    students[dummy_1].push_back(dummy_2);
    students[dummy_2].push_back(dummy_1);
  }

  bool can_detect_dummies = true;
  std::queue<int> students_to_color;
  std::vector<int> students_colored(students_count, 67);

  for (int i = 0; i < students_count; i++) {
    if (students_colored[i] != 67) {
      continue;
    } else {
      students_colored[i] = 0;
      students_to_color.push(i);

      while (students_to_color.size() != 0) {
        int curr_student = students_to_color.front();
        students_to_color.pop();

        for (int near_student : students[curr_student]) {
          if (students_colored[near_student] == 67) {
            students_colored[near_student] = 1 - students_colored[curr_student];
            students_to_color.push(near_student);
          } else {
            if (students_colored[near_student] == students_colored[curr_student]) {
              can_detect_dummies = false;
              break;
            }
          }
        }
      }
    }
  }

  if (can_detect_dummies) {
    std::cout << "YES" << std::endl;
  } else {
    std::cout << "NO" << std::endl;
  }
}
