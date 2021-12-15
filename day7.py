# 12/8/2021
# https://adventofcode.com/2021/day/7

import sys
from math import floor
import statistics

# 16,1,2,0,4,2,7,1,2,14
# 0,1,1,2,2,2,4,7,14,16

# arithmetic series: S_n=n*(a_1 + a_n)/2
# cost to move n spaces: n*(1+n)/2 = (n^2 + n) / 2

# part 1: basically just guessed mean, then when it was wrong, median
# part 2: stumped, looked on reddit, it seems like mean is the answer but don't exactly understand why -- something about min(sum(squares)) being equivalent?
# https://www.reddit.com/r/adventofcode/comments/rar7ty/comment/hnsdcw3/?utm_source=reddit&utm_medium=web2x&context=3
# a more calculus explanation: https://www.reddit.com/r/adventofcode/comments/rawxad/2021_day_7_part_2_i_wrote_a_paper_on_todays/

def get_median(vals):
  s = sorted(vals)
  if len(s) % 2 == 1:
    return s[len(s) // 2]

  i = len(s) // 2
  return (s[i] + s[i - 1]) / 2

def part1():
  fname = sys.argv[1]

  positions = None

  with open(fname, 'r') as f:
    for line in f:
      if positions is None:
        positions = [int(n) for n in line.split(',')]

  # mean = sum(positions) / float(len(positions))
  # mean_rounded = floor(mean)

  median = get_median(positions)

  fuels = [abs(c - median) for c in positions]
  fuel_sum = sum(fuels)

  print("%d (to move to pos %d)" % (fuel_sum, median))

def part1_distance(a, b):
  return abs(a - b)

def part2_distance(a, b):
  d = part1_distance(a, b)
  return d * (d + 1) / 2

def part2():
  fname = sys.argv[1]

  positions = None

  with open(fname, 'r') as f:
    for line in f:
      if positions is None:
        positions = [int(n) for n in line.split(',')]

  mean_unrounded = statistics.mean(positions)
  # the calculus reddit link above says mean is within 0.5 of right answer
  # interestingly, the other non-calc explanation has code that doesn't do this and appears to be wrong
  candidates = [round(mean_unrounded-0.5), round(mean_unrounded+0.5)]

  possible_answers = [sum([part2_distance(p, mean) for p in positions]) for mean in candidates]
  answer = min(possible_answers)

  print("sum %d for mean %f, candidate answers %s" % (answer, mean_unrounded, candidates))

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()