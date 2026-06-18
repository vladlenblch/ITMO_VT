#include <iostream>

using namespace std;

int main() {
    int n;
    cin >> n ;

    long long curr = 0, best = 0;
    for (int i = 0; i < n; i++) {
        int curr_val;
        cin >> curr_val;

        curr = max(0LL, curr + curr_val);
        best = max(best, curr);
    }

    cout << best << endl;
}
