#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

bool compare(const string& a, const string& b) {
  char char_of_ab, char_of_ba;

  for (size_t i = 0; i < (a.size() + b.size()); i++) {
    if (i < a.size()) {
      char_of_ab = a[i];
    } else {
      char_of_ab = b[i - a.size()];
    }

    if (i < b.size()) {
      char_of_ba = b[i];
    } else {
      char_of_ba = a[i - b.size()];
    }

    if (char_of_ab != char_of_ba) {
      return char_of_ab > char_of_ba;
    }
  }

  return false;
}

int main() {
  vector<string> nums;

  string num;
  while (cin >> num) {
    nums.push_back(num);
  }

  sort(nums.begin(), nums.end(), compare);

  for (const string& num : nums) {
    cout << num;
  }
}
