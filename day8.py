# 12/8/2021
# https://adventofcode.com/2021/day/8

import sys
from collections import defaultdict

def read_input():
  fname = sys.argv[1]

  inputs = []

  with open(fname, 'r') as f:
    for line in f:
      parts = line.split(' | ')
      parsed = tuple(["".join(sorted(s.strip())) for s in part.split(" ")] for part in parts)
      inputs.append(parsed)

  return inputs

def part1():
  inputs = read_input()

  count = 0
  for _, query in inputs:
    for s in query:
      if len(s) in [2, 3, 4, 7]:
        count += 1

  print(count)

def inverse(word):
  set_diff = set('abcdefg').difference(set(word))
  return "".join(sorted(list(set_diff)))

def get_mapping(sample):
  # length 2: 1
  # length 3: 7
  # length 4: 4
  # length 5: 2, 3, 5
  # length 6: 0, 6, 9
  # length 7: 8

  mapping = {}

  by_len = defaultdict(lambda: [])
  for word in sample:
    by_len[len(word)].append(word)

  # unique answers
  mapping[by_len[2][0]] = 1
  mapping[by_len[3][0]] = 7
  mapping[by_len[4][0]] = 4
  mapping[by_len[7][0]] = 8
  four = by_len[4][0]
  one = by_len[2][0]

  # length 6

  # First, find 9. It's the digit whose missing segment is in not in 4
  missings = [inverse(word) for word in by_len[6]]
  for i, missing in enumerate(missings):
    if missing not in four:
      nine = by_len[6][i]
      mapping[nine] = 9
      break

  # Next, distinguish between 0 and 6. The missing segment from 6 is in 1, but 0's is not.
  six1, six2 = list(set(by_len[6]).difference(set([nine])))
  six1_inv, six2_inv = inverse(six1), inverse(six2)
  if six1_inv in one:
    mapping[six1] = 6
    mapping[six2] = 0
  else:
    mapping[six1] = 0
    mapping[six2] = 6

  # length 5

  # First, try to find the 3. Both its missing segments are also missing from 1 (the two on the left),
  # and the same is not true for 2 and 5, who each have a missing segment that is not missing from 1.
  missings = [inverse(word) for word in by_len[5]]
  one_set = set(one)
  for i, missing in enumerate(missings):
    missing_from_both = len(set(missing).difference(one_set))
    if missing_from_both == 2:
      three = by_len[5][i]
      mapping[three] = 3
      break

  # Finally, distinguish between 2 and 5. 9 has only one segment that is absent from 5, but it has
  # two segments that are absent from 2.
  five1, five2 = list(set(by_len[5]).difference(set([three])))
  diff = set(nine).difference(set(five1))
  if len(diff) == 1:
    mapping[five1] = 5
    mapping[five2] = 2
  else:
    mapping[five1] = 2
    mapping[five2] = 5

  return mapping

def apply_mapping(query, mapping):
  s = ""

  for word in query:
    s += str(mapping[word])

  return int(s)

def part2():
  inputs = read_input()
  answer = 0

  for sample, query in inputs:
    mapping = get_mapping(sample)
    output = apply_mapping(query, mapping)
    answer += output

  print(answer)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()