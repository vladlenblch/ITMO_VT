#include <iostream>
#include <vector>

using namespace std;

int day_iteration(int bac_count, int bac_multiplier, int bac_exp, int capacity) {
  long long curr_bac_count = bac_count;

  curr_bac_count *= bac_multiplier;

  if (curr_bac_count < bac_exp) {
    return 0;
  }

  curr_bac_count -= bac_exp;

  if (curr_bac_count > capacity) {
    curr_bac_count = capacity;
  }

  return (int)curr_bac_count;
}

int main() {
  int bac_count, bac_multiplier, bac_exp, capacity;
  long long days;
  cin >> bac_count >> bac_multiplier >> bac_exp >> capacity >> days;

  vector<int> first_meet(capacity + 1, -1);
  vector<int> bac_by_day;
  bac_by_day.reserve(capacity + 2);

  int curr_bac_count = bac_count;
  long long curr_day = 0;

  while (true) {
    if (curr_bac_count == 0) {
      cout << 0 << endl;
      return 0;
    }

    if (curr_day == days) {
      cout << curr_bac_count << endl;
      return 0;
    }

    if (first_meet[curr_bac_count] != -1) {
      long long cycle_start = first_meet[curr_bac_count];
      long long cycle_length = curr_day - cycle_start;

      long long index = cycle_start + ((days - cycle_start) % cycle_length);
      cout << bac_by_day[index] << endl;
      return 0;
    }

    first_meet[curr_bac_count] = curr_day;
    bac_by_day.push_back(curr_bac_count);
    curr_bac_count = day_iteration(curr_bac_count, bac_multiplier, bac_exp, capacity);
    curr_day++;
  }
}
