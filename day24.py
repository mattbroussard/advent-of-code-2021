# 12/23/2021
# https://adventofcode.com/2021/day/24

# Note: this solution is not as general as the others; I've hardcoded stuff about the specific
# puzzle input I got. I've also hardcoded file paths for intermediate state since the "precompute graph"
# step from part 1 takes about 3-5min and ~18GB RAM

from time import time
from collections import defaultdict
import sys
import json

A = [1,   1,   1,  26,  26,   1,   1,   26,   1,  26,   1,   26,  26,  26]
B = [12, 12,  12,  -9,  -9,  14,  14,  -10,  15,  -2,  11,  -15,  -9,  -3]
C = [9,   4,   2,   5,   1,   6,  11,   15,   7,  12,  15,    9,  12,  12]

def monad_iteration(w, z=0, i=0):
  p = w != (z % 26) + B[i]
  z = (26 if p else 1) * (z // A[i]) + (w + C[i] if p else 0)
  return z

def compute_monad_checksum(num):
  min_z = 0
  max_z = 0
  z = 0
  for i in range(14):
    w = int(str(num)[i])
    z = monad_iteration(w, z, i)
    min_z = min(min_z, z)
    max_z = max(max_z, z)
  return z, (min_z, max_z)

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    return f.read().strip().splitlines()

def compute_monad_interpreted(instructions, input):
  registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
  input_vals = [int(c) for c in str(input)][::-1]

  def resolve_reg(r):
    if r in registers:
      return registers[r]
    return int(r)

  for inst in instructions:
    parts = inst.strip().split(' ')
    if len(parts) < 3:
      parts.append(None)
    op, r1, r2 = parts
    a = resolve_reg(r1)
    b = resolve_reg(r2) if r2 is not None else None

    if op == 'inp':
      registers[r1] = input_vals.pop()
    elif op == 'add':
      registers[r1] = a + b
    elif op == 'mul':
      registers[r1] = a * b
    elif op == 'div':
      registers[r1] = a // b
    elif op == 'mod':
      registers[r1] = a % b
    elif op == 'eql':
      registers[r1] = 1 if a == b else 0
    else:
      raise Exception('invalid opcode')

  return registers['z']

def test_against_interpreter():
  instructions = read_file()
  iterations = 0

  for n in range(99999999999999, 10000000000000, -1):
    if '0' in str(n):
      continue

    result, _ = compute_monad_checksum(n)
    interpreted_result = compute_monad_interpreted(instructions, n)

    if result == interpreted_result:
      # print("PASS %d: %d" % (n, result))
      pass
    else:
      print("FAIL %d: %d vs %d" % (n, result, interpreted_result))

    iterations += 1
    if iterations > 5000:
      break

def test_z_bounds():
  i = 0
  min_z, max_z = (0, 0)
  for n in range(11111111111111, 99999999999999): # range(99999999999999, 10000000000000, -1):
    if '0' in str(n):
      continue
    i += 1
    if i > 100000:
      break

    _, (z1, z2) = compute_monad_checksum(n)
    min_z = min(min_z, z1)
    max_z = max(max_z, z2)

  print("z: [%d, %d]" % (min_z, max_z))

def test_z_cardinality():
  """
  digit 0: 9 z vals (~9.0x); 0 came up 0 times from 9 (w,z) inputs
  digit 1: 81 z vals (~9.0x); 0 came up 0 times from 81 (w,z) inputs
  digit 2: 729 z vals (~9.0x); 0 came up 0 times from 729 (w,z) inputs
  digit 3: 810 z vals (~1.1x); 0 came up 0 times from 6561 (w,z) inputs
  digit 4: 846 z vals (~1.0x); 0 came up 0 times from 7290 (w,z) inputs
  digit 5: 7614 z vals (~9.0x); 0 came up 0 times from 7614 (w,z) inputs
  digit 6: 68526 z vals (~9.0x); 0 came up 0 times from 68526 (w,z) inputs
  digit 7: 76140 z vals (~1.1x); 0 came up 0 times from 616734 (w,z) inputs
  digit 8: 685260 z vals (~9.0x); 0 came up 0 times from 685260 (w,z) inputs
  digit 9: 714555 z vals (~1.0x); 0 came up 0 times from 6167340 (w,z) inputs
  digit 10: 6430995 z vals (~9.0x); 0 came up 0 times from 6430995 (w,z) inputs
  digit 11: 6687549 z vals (~1.0x); 0 came up 0 times from 57878955 (w,z) inputs
  digit 12: 6463503 z vals (~1.0x); 0 came up 0 times from 60187941 (w,z) inputs
  digit 13: 6435967 z vals (~1.0x); 0 came up 3 times from 58171527 (w,z) inputs
  """
  last_z = set([0])
  for i in range(14):
    cur_z = set()
    zero_count = 0
    for w in range(1,10):
      for z in last_z:
        new_z = monad_iteration(w, z, i)
        if new_z == 0:
          zero_count += 1
        cur_z.add(new_z)

    print("digit %d: %d z vals (~%.1fx); 0 came up %d times from %d (w,z) inputs" % (i, len(cur_z), float(len(cur_z)) / float(len(last_z)), zero_count, len(last_z) * 9))
    last_z = cur_z

def part1_precompute_graph():
  # tables[i = digit index] = {outputZ: list((inputW, inputZ))}
  tables = [defaultdict(list) for _ in range(14)]

  def last_round_z(i):
    return [0] if i == 0 else tables[i-1].keys()

  # Step 1: build the tables (5min, 27GB memory to build with dict + set; 3min 18GB RAM with lists)
  step1_start = time()
  for i in range(14):
    for z in last_round_z(i):
      for w in range(1,10):
        new_z = monad_iteration(w, z, i)
        tables[i][new_z].append((w, z))
    print("Step 1: round %d/14 done, cumulative time: %dms" % (i+1, (time() - step1_start) * 1000))

  key_count = 0
  entry_count = 0
  for table in tables:
    for key in table.keys():
      key_count += 1
      entry_count += len(table[key])

  step1_end = time()
  print("Step 1 done, took %dms, %d total keys, %d total entries" % ((step1_end - step1_start) * 1000, key_count, entry_count))

  # Step 2: Prune the table
  tables[-1] = {0: tables[-1][0]}
  for i in range(12,-1,-1):
    valid_z = set()
    for v in tables[i+1].values():
      for _, iz in v:
        valid_z.add(iz)

    tables[i] = {k: v for k, v in tables[i].items() if k in valid_z}

  key_count = 0
  entry_count = 0
  for table in tables:
    for key in table.keys():
      key_count += 1
      entry_count += len(table[key])

  step2_end = time()
  print("Step 2 done, took %dms, %d remaining keys, %d remaining entries" % ((step2_end - step1_end) * 1000, key_count, entry_count))

  with open('inputs/day24_part1_graph.json', 'w') as f:
    json.dump(tables, f, separators=(',', ':'))

def part1_traverse_graph(agg=max):
  with open('inputs/day24_part1_graph.json', 'r') as f:
    tables = json.load(f)
  # convert keys from string to int (int keys become string when JSONified)
  for i in range(len(tables)):
    tables[i] = {int(k): v for k, v in tables[i].items()}

  def path_value(path):
    v = 0
    for i, pe in enumerate(path):
      w, _ = pe
      v += w * (10 ** i)
    return v

  result = None
  frontier = []
  frontier.append(tuple())
  while len(frontier) > 0:
    path = frontier.pop()
    if len(path) == len(tables):
      value = path_value(path)
      result = agg(result, value) if result is not None else value
      continue

    i = len(tables) - 1 - len(path)
    last_z = 0 if len(path) == 0 else path[-1][1]
    for wz in tables[i][last_z]:
      frontier.append(path + (wz,))

  # sanity check
  monad, _ = compute_monad_checksum(result)
  if monad != 0:
    print("Error: invalid checksum for resulting value %d: %d" % (result, monad))
    return None

  print(result)
  return result

def part2():
  part1_traverse_graph(min)

def main():
  # test_against_interpreter()
  # test_z_bounds()
  # test_z_cardinality()

  # part1_precompute_graph()
  part1_traverse_graph()
  part2()

if __name__ == '__main__':
  main()