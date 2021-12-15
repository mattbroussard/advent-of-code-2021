# 12/8/2021
# https://adventofcode.com/2021/day/5

import sys
from collections import defaultdict

def coord_range(a, b):
  direction = 1 if b >= a else -1
  return range(a, b + direction, direction)

def print_diagram(points):
  max_x = 0
  max_y = 0

  def disp(val):
    if val == 0:
      return '.'
    elif val > 9:
      return 'X'
    else:
      return str(val)

  for x, y in points:
    max_x = max(x, max_x)
    max_y = max(y, max_y)

  for y in range(max_y + 1):
    s = "".join([disp(points[(x, y)]) for x in range(0, max_x + 1)])
    print(s)

def draw_diagonal(points, a, b):
  x1, y1 = a
  x2, y2 = b

  for x, y in zip(coord_range(x1, x2), coord_range(y1, y2)):
    points[(x, y)] += 1

def part1():
  solution(include_diagonal=False)

def part2():
  solution(include_diagonal=True)

def solution(include_diagonal=False):
  fname = sys.argv[1]

  points = defaultdict(lambda: 0)

  with open(fname, 'r') as f:
    for line in f:
      parts = line.split(" -> ")
      x1, y1 = [int(n) for n in parts[0].split(",")]
      x2, y2 = [int(n) for n in parts[1].split(",")]
      # print("Processing line \"%s\" ((%d, %d) -> (%d, %d))" % (line, x1, y1, x2, y2))

      if x1 == x2:
        # vertical
        for y in coord_range(y1, y2):
          points[(x1, y)] += 1
      elif y1 == y2:
        # debug
        # if y1 == 4:
        #   print('********************************************')
        #   print(list(coord_range(x1, x2)))

        # horizontal
        for x in coord_range(x1, x2):
          points[(x, y1)] += 1
      elif include_diagonal:
        draw_diagonal(points, (x1, y1), (x2, y2))
      else:
        # print(line)
        # non-vertical or horizontal; ignore for now but probably will come up in part 2?
        pass

      # print_diagram(points)

      # don't print zeroes
      # for p, v in list(points.items()):
      #   if v == 0:
      #     del points[p]
      # print(dict(points))
      # print("--------")

  # print_diagram(points)

  count = 0
  for pt, c in points.items():
    if c >= 2:
      count += 1

  print(count)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()