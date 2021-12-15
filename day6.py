# 12/8/2021
# https://adventofcode.com/2021/day/6

import sys
from collections import deque

def part1(gen_count=80):
  fname = sys.argv[1]

  queue = deque([0] * 9)

  with open(fname, 'r') as f:
    for line in f:
      for n in line.split(","):
        queue[int(n)] += 1

  for generation in range(gen_count):
    zero = queue.popleft()
    queue.append(0)
    queue[8] += zero
    queue[6] += zero

  count = sum(queue)
  print(count)

def part2():
  part1(256)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()