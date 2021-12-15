# 12/8/2021
# https://adventofcode.com/2021/day/3

import sys
from collections import deque

def build_freqs(vals):
  freqs = None
  for bits in vals:
    if freqs is None:
      freqs = [(0, 0)] * len(bits)

    for i, bit in enumerate(bits):
      zeroes, ones = freqs[i]
      if bit == '0':
        zeroes += 1
      else:
        ones += 1
      freqs[i] = (zeroes, ones)
  return freqs

def part1():
  fname = sys.argv[1]

  vals = []

  with open(fname, 'r') as f:
    for line in f:
      bits = [c for c in line if c in '0123456789']
      vals.append(bits)

  freqs = build_freqs(vals)

  gamma = ''.join(['0' if z > o else '1' for z, o in freqs])
  epsilon = ''.join(['0' if c == '1' else '1' for c in gamma])

  result = int(gamma, 2) * int(epsilon, 2)
  print(result)

def bit_filter(vals, predicate_factory):
  idx = 0
  while len(vals) > 1:
    truncated = [val[idx:] for val in vals]
    predicate = predicate_factory(truncated)
    vals = [v for i, v in enumerate(vals) if predicate(truncated[i])]

    idx += 1

  return vals[0]

def ox_predicate_factory(vals):
  freqs = build_freqs(vals)

  def predicate(bits):
    is_one = bits[0] == '1'
    z, o = freqs[0]
    should_one = o >= z
    return is_one == should_one

  return predicate

def co2_predicate_factory(vals):
  freqs = build_freqs(vals)

  def predicate(bits):
    is_zero = bits[0] == '0'
    z, o = freqs[0]
    should_zero = z <= o
    return is_zero == should_zero

  return predicate

def part2():
  fname = sys.argv[1]

  vals = []

  with open(fname, 'r') as f:
    for line in f:
      bits = [c for c in line if c in '0123456789']
      vals.append(bits)

  ox = bit_filter(vals, ox_predicate_factory)
  co2 = bit_filter(vals, co2_predicate_factory)

  result = int(''.join(ox), 2) * int(''.join(co2), 2)
  print(result)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()