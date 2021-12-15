# 12/6/2021
# https://adventofcode.com/2021/day/1

import sys
from collections import deque

def part1():
  fname = sys.argv[1]
  last = None
  count = 0

  with open(fname, 'r') as f:
    for line in f:
      n = int(line)

      if last is not None:
        if n > last:
          count += 1

      last = n

  print(count)

def part2():
  fname = sys.argv[1]
  last = None
  count = 0

  window = deque()
  win_size = 3

  with open(fname, 'r') as f:
    for line in f:
      n = int(line)

      window.append(n)
      if len(window) > win_size:
        window.popleft()

      if len(window) == win_size:
        win_sum = sum(window)

        if last is not None:
          if win_sum > last:
            count += 1

        last = win_sum

  print(count)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()