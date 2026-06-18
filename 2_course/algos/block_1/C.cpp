#include <iostream>
#include <map>
#include <stack>
#include <string>
#include <vector>

using namespace std;

bool is_number(const string& s) {
  if (s[0] == '-') {
    for (int i = 1; i < (int)s.size(); i++) {
      if (s[i] < '0' || s[i] > '9') {
        return false;
      }
    }

    return true;
  }

  for (int i = 0; i < (int)s.size(); i++) {
    if (s[i] < '0' || s[i] > '9') {
      return false;
    }
  }

  return true;
}

int main() {
  stack<vector<string>> history_stack;
  map<string, stack<long long>> scope_map;

  history_stack.push(vector<string>());

  string line;
  while (getline(cin, line)) {
    if (line == "{") {
      history_stack.push(vector<string>());
      continue;
    }

    if (line == "}") {
      for (const string& elem : history_stack.top()) {
        scope_map[elem].pop();
      }

      history_stack.pop();
      continue;
    }

    size_t equals_pos = line.find('=');
    string left_arg = line.substr(0, equals_pos);
    string right_arg = line.substr(equals_pos + 1);

    if (is_number(right_arg)) {
      long long value = stoll(right_arg);
      scope_map[left_arg].push(value);
      history_stack.top().push_back(left_arg);
    } else {
      auto& st = scope_map[right_arg];
      long long value;
      if (st.empty()) {
        value = 0;
      } else {
        value = st.top();
      }

      scope_map[left_arg].push(value);
      history_stack.top().push_back(left_arg);
      cout << value << endl;
    }
  }
}
