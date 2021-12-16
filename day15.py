# 12/14/2021
# https://adventofcode.com/2021/day/15

import sys
import heapq

def read_input():
  fname = sys.argv[1]

  table = []

  with open(fname, 'r') as f:
    for line in f:
      row = [int(n) for n in line.strip()]
      if len(row) > 0:
        table.append(row)

  return table

def neighbors(table, point):
  x, y = point
  for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    if x + dx < 0 or y + dy < 0 or x + dx >= len(table[0]) or y + dy >= len(table):
      continue
    yield (x + dx, y + dy)

def part1(table=read_input()):
  start = (0, 0)
  end = (len(table[0]) - 1, len(table) - 1)

  solution = None

  # tuples on the queue have:
  #  - 0: cost so far
  #  - 1: path so far as list of point tuples
  frontier = [(0, [start])]
  seen = set([start])
  while len(frontier) > 0:
    cost, path = heapq.heappop(frontier)
    cur = path[-1]

    for n in neighbors(table, cur):
      if n in seen:
        continue

      x, y = n
      new_entry = (cost + table[y][x], path + [n])

      if n == end:
        solution = new_entry
        frontier = []
        break

      heapq.heappush(frontier, new_entry)

      # it's ok to consider things seen at enqueue time rather than dequeue since we are by definition
      # at the cheapest point adjacent to n already and all inbound edges to n weigh the same. If this
      # weren't true, we would need to consider other possible paths to n that appear in iterations before
      # we dequeue n.
      seen.add(n)

  if solution is not None:
    print(solution[0])
  else:
    print("No solution...?")

class TiledRow:
  def __init__(self, underlying_row, x_tiles, y_offset):
    self.underlying_row = underlying_row
    self.x_tiles = x_tiles
    self.y_offset = y_offset

  def __getitem__(self, key):
    x_offset = key // len(self.underlying_row)
    x = key % len(self.underlying_row)
    adjusted = self.underlying_row[x] + x_offset + self.y_offset
    wrapped_adjusted = ((adjusted - 1) % 9) + 1
    return wrapped_adjusted

  def __len__(self):
    return len(self.underlying_row) * self.x_tiles

class TiledMap:
  def __init__(self, underlying_table, x_tiles, y_tiles):
    self.underlying_table = underlying_table
    self.x_tiles = 5
    self.y_tiles = 5

  def __getitem__(self, key):
    y_offset = key // len(self.underlying_table)
    y = key % len(self.underlying_table)
    return TiledRow(self.underlying_table[y], self.x_tiles, y_offset)

  def __len__(self):
    return len(self.underlying_table) * self.y_tiles

def part2():
  table = read_input()
  part1(TiledMap(table, 5, 5))

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()