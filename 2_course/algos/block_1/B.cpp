#include <iostream>
#include <stack>
#include <vector>

using namespace std;

int main() {
  string line;
  cin >> line;

  int animals_count = line.size() / 2;
  stack<pair<int, char>> st;
  vector<int> animals_in_traps(animals_count + 1, 0);
  int animal_id = 0;
  int trap_id = 0;

  for (char ch : line) {
    if (islower(ch)) {
      animal_id++;
    } else {
      trap_id++;
    }

    if (!st.empty()) {
      char top_ch = st.top().second;
      bool same_letter = tolower(top_ch) == tolower(ch);
      bool lower_top_upper_curr = islower(top_ch) && isupper(ch);
      bool upper_top_lower_curr = isupper(top_ch) && islower(ch);
      bool diff_case = lower_top_upper_curr || upper_top_lower_curr;

      if (same_letter && diff_case) {
        if (islower(ch)) {
          int trap_num = st.top().first;
          animals_in_traps[trap_num] = animal_id;
        } else {
          int animal_num = st.top().first;
          animals_in_traps[trap_id] = animal_num;
        }

        st.pop();
        continue;
      }
    }

    if (islower(ch)) {
      st.push({animal_id, ch});
    } else {
      st.push({trap_id, ch});
    }
  }

  if (st.empty()) {
    cout << "Possible\n";
    for (int i = 1; i < (int)animals_in_traps.size(); i++) {
      cout << animals_in_traps[i] << " ";
    }
  } else {
    cout << "Impossible\n";
  }
}
