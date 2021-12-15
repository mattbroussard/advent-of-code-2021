# 12/9/2021
# https://adventofcode.com/2021/day/10

import sys
from collections import deque
import statistics

def read_input():
  fname = sys.argv[1]

  with open(fname, 'r') as f:
    return [line.strip() for line in f]

mapping = {'(': ')', '[': ']', '{': '}', '<': '>'}
p1_score_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
p2_score_map = {')': 1, ']': 2, '}': 3, '>': 4}

def classify(line):
  stack = deque()

  for c in line:
    if c in mapping:
      stack.append(c)
      continue

    # stack is empty but we have another character, corrupt
    if len(stack) == 0:
      return 'corrupt', c

    expected = mapping[stack[-1]]
    if expected == c:
      stack.pop()
      continue

    # character is not what we expected, corrupt
    return 'corrupt', c

  # stack is not empty but we're out of characters: incomplete
  if len(stack) != 0:
    fix = "".join([mapping[c] for c in stack][::-1])
    return 'incomplete', fix

  return 'valid', None

def part1():
  lines = read_input()
  score = 0

  for line in lines:
    status, last = classify(line)
    if status == 'corrupt':
      score += p1_score_map[last]

  print(score)

def part2():
  lines = read_input()

  scores = []

  for line in lines:
    status, fix = classify(line)
    if status == 'incomplete':
      score = 0
      for c in fix:
        score = score * 5 + p2_score_map[c]
      scores.append(score)

  answer = statistics.median(sorted(scores))
  print(answer)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
