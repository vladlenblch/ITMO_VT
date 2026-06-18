#include <iostream>
#include <vector>

using namespace std;

int main() {
  int flowers_count;
  cin >> flowers_count;

  int max_len = 2, curr_max_len = 2, start_index_max_len = 0, end_index_max_len = 1;

  if (flowers_count < 3) {
    cout << 1 << " " << flowers_count << endl;
    return 0;
  }

  int first_elem, second_elem;
  cin >> first_elem >> second_elem;

  for (int i = 0; i < flowers_count - 2; i++) {
    int curr_elem;
    cin >> curr_elem;

    if (!(first_elem == second_elem && second_elem == curr_elem)) {
      curr_max_len++;
    } else {
      if (curr_max_len > max_len) {
        max_len = curr_max_len;
        start_index_max_len = i - curr_max_len + 2;
        end_index_max_len = i + 1;
      }

      curr_max_len = 2;
    }

    first_elem = second_elem;
    second_elem = curr_elem;
  }

  if (curr_max_len > max_len) {
    max_len = curr_max_len;
    start_index_max_len = flowers_count - curr_max_len;
    end_index_max_len = flowers_count - 1;
  }

  cout << start_index_max_len + 1 << " " << end_index_max_len + 1 << endl;
  return 0;
}
