#include <algorithm>
#include <iostream>
#include <vector>

struct DSU {
  std::vector<int> parents;

  DSU(int n) {
    parents.resize(n + 1);
    for (int i = 1; i < n + 1; i++) {
      parents[i] = i;
    }
  }

  int find(int node) {
    if (node == parents[node]) {
      return node;
    }

    return parents[node] = find(parents[node]);
  }

  void unite(int node1, int node2) {
    node1 = find(node1);
    node2 = find(node2);

    if (node1 != node2) {
      parents[node2] = node1;
    }
  }
};

int main() {
  int hubs_count, possible_hub_connections_count;
  std::cin >> hubs_count >> possible_hub_connections_count;

  std::vector<std::pair<std::pair<int, int>, int>> hubs;
  for (int i = 0; i < possible_hub_connections_count; i++) {
    int hub1, hub2, dist;
    std::cin >> hub1 >> hub2 >> dist;

    hubs.push_back({
        {hub1, hub2},
        dist
    });
  }

  std::sort(hubs.begin(), hubs.end(), [](const auto& a, const auto& b) {
    return a.second < b.second;
  });

  int max_dist = 0;
  DSU dsu(hubs_count);
  std::vector<std::pair<int, int>> results;

  for (auto& h : hubs) {
    int first_hub = h.first.first;
    int second_hub = h.first.second;

    if (dsu.find(first_hub) != dsu.find(second_hub)) {
      dsu.unite(first_hub, second_hub);
      results.push_back({first_hub, second_hub});
      max_dist = std::max(max_dist, h.second);
    }
  }

  std::cout << max_dist << std::endl;
  std::cout << results.size() << std::endl;
  for (auto& r : results) {
    std::cout << r.first << " " << r.second << std::endl;
  }
}
