# 12/10/2021
# https://adventofcode.com/2021/day/11

import sys

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

  for dy in range(-1, 2):
    for dx in range(-1, 2):
      if dx == 0 and dy == 0:
        continue
      if x + dx < 0 or y + dy < 0 or x + dx >= len(table[0]) or y + dy >= len(table):
        continue

      yield (x + dx, y + dy)

def increment(table):
  for row in table:
    for i in range(len(row)):
      row[i] += 1

def flash(table):
  flashed = 0
  for y in range(len(table)):
    for x in range(len(table[y])):
      if table[y][x] > 9:
        flashed += 1
        table[y][x] = 0
        for nx, ny in neighbors(table, (x, y)):
          # don't increment neighboring cells that have already flashed, apparently
          if table[ny][nx] == 0:
            continue

          table[ny][nx] += 1
  return flashed

def print_table(table):
  for row in table:
    print("".join(str(v) if v <= 9 else 'X' for v in row))

def all_flashed(table):
  for row in table:
    for cell in row:
      if cell != 0:
        return False
  return True

def part1():
  table = read_input()

  flash_count = 0

  for step in range(100):
    increment(table)

    reflash_count = 1
    flashed = flash(table)
    while flashed != 0:
      flash_count += flashed
      flashed = flash(table)
      reflash_count += 1

    # print('After step %d, %d flashes so far (%d subrounds this step)' % (step + 1, flash_count, reflash_count))
    # print_table(table)

  print(flash_count)

def part2():
  table = read_input()

  step = 0
  while True:
    step += 1

    increment(table)
    flashed = flash(table)
    while flashed != 0:
      flashed = flash(table)

    if all_flashed(table):
      break

  print(step)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
