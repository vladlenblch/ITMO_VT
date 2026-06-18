#include <iostream>
#include <vector>

using namespace std;

void sort_by_weights(vector<int>& letters_more_than_one, vector<long long>& weights) {
  int len = (int)letters_more_than_one.size();
  for (int i = 0; i < len - 1; i++) {
    for (int j = 0; j < len - 1 - i; j++) {
      if (weights[letters_more_than_one[j + 1]] > weights[letters_more_than_one[j]]) {
        swap(letters_more_than_one[j], letters_more_than_one[j + 1]);
      }
    }
  }
}

int main() {
  string line;
  cin >> line;

  vector<long long> weights(26);
  for (int i = 0; i < 26; i++) {
    cin >> weights[i];
  }

  vector<int> letters_counts(26, 0);
  for (char ch : line) {
    letters_counts[ch - 'a']++;
  }

  vector<int> letters_more_than_one;
  for (int i = 0; i < 26; i++) {
    if (letters_counts[i] > 1) {
      letters_more_than_one.push_back(i);
    }
  }

  sort_by_weights(letters_more_than_one, weights);

  int line_len = (int)line.size();
  int left = 0;
  int right = line_len - 1;
  string sorted_line(line_len, '0');

  for (int shift : letters_more_than_one) {
    if (left == right) {
      break;
    }

    sorted_line[left] = char('a' + shift);
    left++;
    sorted_line[right] = char('a' + shift);
    right--;
    letters_counts[shift] -= 2;
  }

  for (int i = 0; i < 26; i++) {
    while (letters_counts[i] > 0) {
      while (left <= right && sorted_line[left] != '0') {
        left++;
      }

      if (left > right) {
        break;
      }

      sorted_line[left] = char('a' + i);
      letters_counts[i]--;
    }
  }

  cout << sorted_line;
}
