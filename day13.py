# 12/13/2021
# https://adventofcode.com/2021/day/13

import sys

def read_input():
  fname = sys.argv[1]

  points = set()
  folds = []

  with open(fname, 'r') as f:
    for line in f:
      if ',' in line:
        point = tuple(int(n) for n in line.split(','))
        points.add(point)

      if 'fold along' in line:
        value = int(line.split('=')[1])
        if 'x=' in line:
          folds.append((value, None))
        else:
          folds.append((None, value))

  return points, folds

def eligible_for_reflection(fold, point):
  fx, fy = fold
  px, py = point
  if fx is not None:
    return px >= fx
  else:
    return py >= fy

def reflect_x(point, x):
  px, py = point
  nx = x - (px - x)
  return (nx, py)

def reflect_y(point, y):
  px, py = point
  ny = y - (py - y)
  return (px, ny)

def reflect(point, fold):
  x, y = fold
  if x is not None:
    return reflect_x(point, x)
  else:
    return reflect_y(point, y)

def print_matrix(points):
  max_x, max_y = 0, 0
  for x, y in points:
    max_x = max(x, max_x)
    max_y = max(y, max_y)

  for y in range(max_y + 1):
    print("".join("#" if (x, y) in points else ' ' for x in range(max_x + 1)))

def part1(fold_limit=1):
  points, folds = read_input()

  for i, fold in enumerate(folds):
    if i >= fold_limit:
      break

    for point in list(points):
      if eligible_for_reflection(fold, point):
        points.remove(point)
        points.add(reflect(point, fold))

  print(len(points))
  return points

def part2():
  points = part1(fold_limit=float('inf'))
  print_matrix(points)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
