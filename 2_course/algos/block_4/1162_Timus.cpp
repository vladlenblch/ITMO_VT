#include <iostream>
#include <vector>

struct exchange_info {
  int from;
  int to;
  double rate;
  double comission;
};

int main() {
  int currencies_count, exchange_points_count;
  int start_currency_number;
  double start_currency_amount;

  std::cin >> currencies_count >> exchange_points_count;
  std::cin >> start_currency_number >> start_currency_amount;

  std::vector<exchange_info> graph;
  for (int i = 0; i < exchange_points_count; i++) {
    int currency_a, currency_b;
    double rate_a_to_b, comission_a_to_b;
    double rate_b_to_a, comission_b_to_a;

    std::cin >> currency_a >> currency_b;
    std::cin >> rate_a_to_b >> comission_a_to_b;
    std::cin >> rate_b_to_a >> comission_b_to_a;

    graph.push_back({currency_a, currency_b, rate_a_to_b, comission_a_to_b});
    graph.push_back({currency_b, currency_a, rate_b_to_a, comission_b_to_a});
  }

  std::vector<double> money(currencies_count + 1, 0.0);
  money[start_currency_number] = start_currency_amount;

  for (int i = 0; i < currencies_count - 1; i++) {
    for (auto& g : graph) {
      if (money[g.from] > g.comission) {
        double new_money = (money[g.from] - g.comission) * g.rate;

        if (new_money > money[g.to]) {
          money[g.to] = new_money;
        }
      }
    }
  }

  bool can_become_dollar_multimillionaire = false;

  for (auto& g : graph) {
    if (money[g.from] > g.comission) {
      double new_money = (money[g.from] - g.comission) * g.rate;

      if (new_money > money[g.to]) {
        can_become_dollar_multimillionaire = true;
        break;
      }
    }
  }

  if (can_become_dollar_multimillionaire) {
    std::cout << "YES";
  } else {
    std::cout << "NO";
  }
}
