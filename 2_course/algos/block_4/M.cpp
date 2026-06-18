#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

int main() {
  int rows, cols;
  int start_row, start_col;
  int end_row, end_col;
  std::cin >> rows >> cols >> start_row >> start_col >> end_row >> end_col;

  std::vector<std::string> map;
  map.reserve(rows);
  for (int i = 0; i < rows; i++) {
    std::string row;
    std::cin >> row;
    map.push_back(row);
  }

  start_row--;
  start_col--;
  end_row--;
  end_col--;

  std::vector<std::vector<int>> distances(rows, std::vector<int>(cols));
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      if (!(i == start_row && j == start_col)) {
        distances[i][j] = 1000000000;
      }
    }
  }

  std::vector<std::vector<std::pair<int, int>>> parents(
      rows, std::vector<std::pair<int, int>>(cols)
  );
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      parents[i][j] = {-1, -1};
    }
  }

  std::priority_queue<
      std::pair<int, std::pair<int, int>>,
      std::vector<std::pair<int, std::pair<int, int>>>,
      std::greater<std::pair<int, std::pair<int, int>>>>
      min_distance;
  min_distance.push({
      0, {start_row, start_col}
  });

  std::vector<int> neighbour_rows = {1, -1, 0, 0};
  std::vector<int> neighbour_cols = {0, 0, -1, 1};

  while (min_distance.size() != 0) {
    std::pair<int, std::pair<int, int>> curr = min_distance.top();
    int curr_distance = curr.first;
    int curr_row = curr.second.first;
    int curr_col = curr.second.second;
    min_distance.pop();

    if (curr_distance != distances[curr_row][curr_col]) {
      continue;
    }

    for (int i = 0; i < 4; i++) {
      int neighbour_row = curr_row + neighbour_rows[i];
      int neighbour_col = curr_col + neighbour_cols[i];

      bool inside_map =
          0 <= neighbour_row && neighbour_row < rows && 0 <= neighbour_col && neighbour_col < cols;
      if (!inside_map) {
        continue;
      }

      if (map[neighbour_row][neighbour_col] == '#') {
        continue;
      }

      int new_distance;
      if (map[neighbour_row][neighbour_col] == '.') {
        new_distance = curr_distance + 1;
      } else {
        new_distance = curr_distance + 2;
      }

      if (new_distance < distances[neighbour_row][neighbour_col]) {
        distances[neighbour_row][neighbour_col] = new_distance;
        parents[neighbour_row][neighbour_col] = {curr_row, curr_col};

        min_distance.push({
            new_distance, {neighbour_row, neighbour_col}
        });
      }
    }
  }

  if (distances[end_row][end_col] == 1000000000) {
    std::cout << -1 << std::endl;
  } else {
    std::cout << distances[end_row][end_col] << std::endl;

    std::string path;
    int curr_row = end_row;
    int curr_col = end_col;
    while (curr_row != start_row || curr_col != start_col) {
      int prev_row = parents[curr_row][curr_col].first;
      int prev_col = parents[curr_row][curr_col].second;

      if (prev_row == curr_row + 1) {
        path += 'N';
      } else if (prev_col == curr_col - 1) {
        path += 'E';
      } else if (prev_row == curr_row - 1) {
        path += 'S';
      } else if (prev_col == curr_col + 1) {
        path += 'W';
      }

      curr_row = prev_row;
      curr_col = prev_col;
    }

    std::reverse(path.begin(), path.end());
    std::cout << path << std::endl;
  }
}
