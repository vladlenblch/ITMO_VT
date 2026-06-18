#include <iostream>
#include <vector>

using namespace std;

long long get_max_fights(int fighters, int teams) {
    int fighters_per_team = fighters / teams;
    int extra_fighters = fighters - fighters_per_team * teams;
    long long total_fights = 0;

    vector<int> team_sizes(teams, fighters_per_team);
    for (int i = 0; i < extra_fighters; i++) {
        team_sizes[i]++;
    }

    for (int i = 0; i < (int)team_sizes.size(); i++) {
        total_fights += team_sizes[i] * (fighters - team_sizes[i]);
    }

    return total_fights / 2;
}

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        int fighters, teams;
        cin >> fighters >> teams;

        cout << get_max_fights(fighters, teams) << endl;
    }
}
