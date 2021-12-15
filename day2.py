# 12/6/2021
# https://adventofcode.com/2021/day/2

import sys
from collections import deque

def part1():
  fname = sys.argv[1]
  
  hpos = 0
  depth = 0

  with open(fname, 'r') as f:
    for line in f:
      cmd, valstr = line.split(" ")
      val = int(valstr)

      if cmd == "forward":
        hpos += val
      elif cmd == "down":
        depth += val
      elif cmd == "up":
        depth -= val

  result = hpos * depth

  print(result)

def part2():
  fname = sys.argv[1]

  hpos = 0
  depth = 0
  aim = 0

  with open(fname, 'r') as f:
    for line in f:
      cmd, valstr = line.split(" ")
      val = int(valstr)

      if cmd == "forward":
        hpos += val
        depth += aim * val
      elif cmd == "down":
        aim += val
      elif cmd == "up":
        aim -= val

  result = hpos * depth

  print(result)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()