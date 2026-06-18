#include <iostream>
#include <vector>

using namespace std;

bool can_place(long long diff, const vector<int>& coords, int traps_count, int cows_count) {
  int placed = 1;
  long long last_cow_coord = coords[0];

  for (int i = 1; i < traps_count; i++) {
    if (coords[i] - last_cow_coord >= diff) {
      last_cow_coord = coords[i];
      placed++;
      if (placed == cows_count) {
        return true;
      }
    }
  }

  return false;
}

int main() {
  int traps_count, cows_count;
  cin >> traps_count >> cows_count;

  vector<int> coords;
  for (int i = 0; i < traps_count; i++) {
    int trap_coord;
    cin >> trap_coord;
    coords.push_back(trap_coord);
  }

  long long left = 0;
  long long right = coords[traps_count - 1] - coords[0];

  while (left < right) {
    long long mid = (left + right + 1) / 2;
    if (can_place(mid, coords, traps_count, cows_count)) {
      left = mid;
    } else {
      right = mid - 1;
    }
  }

  cout << left;
}
