# 12/14/2021
# https://adventofcode.com/2021/day/14

import sys
from collections import defaultdict
def read_input():
  fname = sys.argv[1]

  template = None
  rules = {}

  with open(fname, 'r') as f:
    for line in f:
      l = line.strip()
      if len(l) == 0:
        continue

      if '->' in l:
        k, v = l.split(' -> ')
        rules[k] = v
      elif template is None:
        template = l

  return template, rules

def part1_answer(counts):
  letter_counts = defaultdict(lambda: 0)
  for pair, count in counts.items():
    letter = pair[0]
    letter_counts[letter] += count

  letters_by_freq = sorted(letter_counts.items(), key=lambda item: item[1])
  most_common = letters_by_freq[-1][1]
  least_common = letters_by_freq[0][1]
  answer = most_common - least_common

  return answer

def polymer_length(counts):
  return sum(counts.values())

def brute_force_step(template, rules):
  i = 0
  while i < len(template) - 1:
    pair = template[i:i+2]
    if pair in rules:
      template = template[:i+1] + rules[pair] + template[i+1:]
      i += 1
    i += 1

  return template

def part1_brute():
  template, rules = read_input()

  for step in range(10):
    template = brute_force_step(template, rules)

  letter_counts = defaultdict(lambda: 0)
  for c in template:
    letter_counts[c] += 1

  letters_by_freq = sorted(letter_counts.items(), key=lambda item: item[1])
  most_common = letters_by_freq[-1][1]
  least_common = letters_by_freq[0][1]
  answer = most_common - least_common

  print(answer)

def part1(step_count=10):
  template, rules = read_input()
  brute = template

  # We add a dummy character to the template so that every real character can be the first
  # character in a pair. This will be important both for the counting process at the end and
  # the initial population of the counts map below.
  template += '_'

  counts = defaultdict(lambda: 0)
  for i in range(len(template) - 1):
    counts[template[i:i+2]] += 1

  for step in range(step_count):
    updates = defaultdict(lambda: 0)

    for pair in list(counts.keys()):
      if counts[pair] == 0:
        del counts[pair]
        continue

      if pair not in rules:
        continue

      replace_count = counts[pair]
      updates[pair] -= replace_count

      updates[pair[0] + rules[pair]] += replace_count
      updates[rules[pair] + pair[1]] += replace_count

    for pair, count in updates.items():
      counts[pair] += count
      if counts[pair] == 0:
        del counts[pair]

    # comment this out to enable debug prints & simultaneous brute force calcuation
    continue

    brute = brute_force_step(brute, rules)
    brute_counts = defaultdict(lambda: 0)
    for i in range(len(brute) - 1):
      brute_counts[brute[i:i+2]] += 1

    print('Step %d: %d/%d length, %d answer; %s' % (step + 1, polymer_length(counts), len(brute), part1_answer(counts), brute))
    print(dict(counts))
    print(dict(brute_counts))

  print(part1_answer(counts))

def part2():
  part1(40)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
