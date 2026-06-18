#include <algorithm>
#include <iostream>
#include <unordered_set>
#include <vector>

long long to_val(int week_idx, int day_idx, int days_count) {
  return 1LL * week_idx * (days_count + 1LL) + day_idx;
}

int main() {
  int weeks_count, days_count, bad_days_count;
  std::cin >> weeks_count >> days_count >> bad_days_count;

  std::vector<std::vector<int>> bad_rows(weeks_count + 1);
  std::vector<std::vector<int>> bad_cols(days_count + 1);

  for (int i = 0; i < bad_days_count; ++i) {
    int week_idx, day_idx;
    std::cin >> week_idx >> day_idx;

    bad_rows[week_idx].push_back(day_idx);
    bad_cols[day_idx].push_back(week_idx);
  }

  long long horizontal_segments = 0, vertical_segments = 0;
  long long row_single_count = 0, col_single_count = 0, intersected_single_count = 0;

  std::unordered_set<long long> single_in_rows;
  single_in_rows.reserve((size_t)bad_days_count + weeks_count + 10);

  for (int row = 1; row <= weeks_count; row++) {
    auto& cols = bad_rows[row];
    std::sort(cols.begin(), cols.end());

    int segment_start = 1;
    for (int bad_day : cols) {
      int segment_length = bad_day - segment_start;
      if (segment_length > 0) {
        horizontal_segments++;
      }
      if (segment_length == 1) {
        row_single_count++;
        single_in_rows.insert(to_val(row, segment_start, days_count));
      }
      segment_start = bad_day + 1;
    }

    int segment_length = days_count - segment_start + 1;
    if (segment_length > 0) {
      horizontal_segments++;
    }
    if (segment_length == 1) {
      row_single_count++;
      single_in_rows.insert(to_val(row, segment_start, days_count));
    }
  }

  for (int col = 1; col <= days_count; col++) {
    auto& rows = bad_cols[col];
    std::sort(rows.begin(), rows.end());

    int segment_start = 1;
    for (int bad_week : rows) {
      int segment_length = bad_week - segment_start;
      if (segment_length > 0) {
        vertical_segments++;
      }
      if (segment_length == 1) {
        col_single_count++;
        if (single_in_rows.count(to_val(segment_start, col, days_count))) {
          intersected_single_count++;
        }
      }
      segment_start = bad_week + 1;
    }

    int segment_length = weeks_count - segment_start + 1;
    if (segment_length > 0) {
      vertical_segments++;
    }
    if (segment_length == 1) {
      col_single_count++;
      if (single_in_rows.count(to_val(segment_start, col, days_count))) {
        intersected_single_count++;
      }
    }
  }

  std::cout
      << (horizontal_segments + vertical_segments - row_single_count - col_single_count +
          intersected_single_count);
}
