#include <iostream>
#include <vector>

using namespace std;

int main() {
  int count, free;
  cin >> count >> free;

  vector<int> count_prices(10001, 0);
  for (int i = 0; i < count; i++) {
    int price;
    cin >> price;
    count_prices[price]++;
  }

  long long total_sum = 0, iter = 0;
  for (int i = 10000; i > 0; i--) {
    while (count_prices[i] > 0) {
      iter++;
      if (iter % free != 0) {
        total_sum += i;
      }

      count_prices[i]--;
    }
  }

  cout << total_sum;
}
