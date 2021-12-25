# 12/24/2021
# https://adventofcode.com/2021/day/25

import sys

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    lines = [list(line.strip()) for line in f.read().strip().splitlines()]
    return lines

def simulate_step(table):
  moved = 0

  # simulate right-moving
  for row in table:
    x = 0
    right_moves = []
    while x < len(row):
      if row[x] == '>':
        x2 = (x + 1) % len(row)
        next_cell = row[x2]
        if next_cell == '.':
          right_moves.append(x)

      x += 1

    for x in right_moves:
      x2 = (x + 1) % len(row)
      row[x2] = '>'
      row[x] = '.'
      moved += 1

  # simulate down-moving
  for x in range(len(table[0])):
    y = 0
    down_moves = []
    while y < len(table):
      if table[y][x] == 'v':
        y2 = (y + 1) % len(table)
        next_cell = table[y2][x]
        if next_cell == '.':
          down_moves.append(y)

      y += 1

    for y in down_moves:
      y2 = (y + 1) % len(table)
      table[y2][x] = 'v'
      table[y][x] = '.'
      moved += 1

  return moved

def print_table(table):
  for row in table:
    print("".join(row))

def part1():
  table = read_file()

  steps = 0
  while True:
    result = simulate_step(table)
    steps += 1

    # print("\nAfter %d steps:" % (steps,))
    # print_table(table)

    if result == 0:
      break

  print(steps)

def main():
  part1()

if __name__ == '__main__':
  main()
