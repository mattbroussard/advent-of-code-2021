# 12/8/2021
# https://adventofcode.com/2021/day/9

import sys
from collections import deque

def read_input():
  fname = sys.argv[1]

  rows = []

  with open(fname, 'r') as f:
    for line in f:
      row = [int(c) for c in line.strip()]
      rows.append(row)

  return rows

def neighbors(table, point):
  x, y = point
  for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    if x + dx < 0 or y + dy < 0 or x + dx >= len(table[0]) or y + dy >= len(table):
      continue
    yield (x + dx, y + dy)

def is_low(table, point):
  x, y = point

  for nx, ny in neighbors(table, point):
    # NB: if 2 of the same value are adjacent, neither are considered low points
    if table[ny][nx] <= table[y][x]:
      return False

  return True

def part1():
  table = read_input()
  # print(table)

  low_points = []

  for y in range(len(table)):
    for x in range(len(table[0])):
      pt = (x, y)
      if is_low(table, pt):
        low_points.append(pt)

  # print(low_points)
  risks = [table[y][x] + 1 for x, y in low_points]
  # print(risks)
  total_risk = sum(risks)

  print(total_risk)

def part2():
  table = read_input()
  low_points = []

  for y in range(len(table)):
    for x in range(len(table[0])):
      pt = (x, y)
      if is_low(table, pt):
        low_points.append(pt)

  basin_sizes = {}
  for pt in low_points:
    basin_sizes[pt] = 0

    frontier = deque()
    frontier.append(pt)
    seen = set([pt])
    while len(frontier) > 0:
      el = frontier.popleft()
      basin_sizes[pt] += 1

      for n in neighbors(table, el):
        nx, ny = n
        if n in seen or table[ny][nx] == 9:
          continue

        seen.add(n)
        frontier.append(n)

  all_sizes = sorted(list(basin_sizes.values()))
  top_3 = all_sizes[-3:]

  answer = 1
  for size in top_3:
    answer *= size
  print(answer)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
