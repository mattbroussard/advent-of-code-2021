# 12/18/2021
# https://adventofcode.com/2021/day/18

import sys
import json
from copy import deepcopy

from colors import colors

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    lines = f.read().splitlines()
    return [json.loads(line) for line in lines]

def stringify(num):
  color_set = [
    colors.fg.red,
    colors.fg.green,
    colors.fg.blue,
    colors.fg.cyan,

    # these bold colors correspond to bracket depths that are eligible for exploding
    colors.fg.purple + colors.bold,
    colors.fg.yellow + colors.bold,
    colors.fg.pink + colors.bold
  ]

  d = -1
  def colorize(c):
    nonlocal d
    if c == '[':
      d += 1
      return color_set[d % len(color_set)] + c + colors.reset
    elif c == ']':
      ret = color_set[d % len(color_set)] + c + colors.reset
      d -= 1
      return ret
    return c

  s = json.dumps(num, separators=(',', ':'))
  s = "".join(colorize(c) for c in s)
  return s

def leftmost(root):
  ptr = tuple()
  while isinstance(root, list):
    ptr += (0,)
    root = root[0]
  return ptr

def rightmost(root):
  ptr = tuple()
  while isinstance(root, list):
    ptr += (1,)
    root = root[1]
  return ptr

def next(root, ptr):
  v = get(root, ptr)
  # leaf
  if isinstance(v, int):
    # right leaf
    if ptr[-1] == 1:
      # already right-most
      if 0 not in ptr:
        return None

      # go up until we are not a right child, then one more to that node's parent
      while ptr[-1] == 1:
        ptr = ptr[:-1]
      ptr = ptr[:-1]
      return ptr

    # left leaf
    else:
      # return parent
      return ptr[:-1]

  # list node
  else:
    # return leftmost leaf of right subtree
    return ptr + (1,) + leftmost(v[1])

def prev(root, ptr):
  v = get(root, ptr)
  # leaf
  if isinstance(v, int):
    # right leaf
    if ptr[-1] == 1:
      # return parent
      return ptr[:-1]

    # left leaf
    else:
      # already left-most
      if 1 not in ptr:
        return None

      # go up until we are not a left child, then one more to that node's parent
      while ptr[-1] == 0:
        ptr = ptr[:-1]
      ptr = ptr[:-1]
      return ptr

  # list node
  else:
    # return rightmost leaf of left subtree
    return ptr + (0,) + rightmost(v[0])

def depth(ptr):
  return len(ptr)

def explode(root, ptr):
  v = get(root, ptr)
  if not isinstance(v, list):
    raise Exception('invalid call to explode')
  a, b = v
  if not isinstance(a, int) or not isinstance(b, int):
    raise Exception('invalid call to explode')

  # print(' - next: exploding %s at %s' % (v, ptr))

  # first step left will be left child, we need to start 2 steps left
  left_neighbor = prev(root, ptr)
  left_neighbor = prev(root, left_neighbor)
  while left_neighbor is not None and not isinstance(get(root, left_neighbor), int):
    left_neighbor = prev(root, left_neighbor)

  # first step right will be right child, we need to start 2 steps right
  right_neighbor = next(root, ptr)
  right_neighbor = next(root, right_neighbor)
  while right_neighbor is not None and not isinstance(get(root, right_neighbor), int):
    right_neighbor = next(root, right_neighbor)

  # print(' - left: %s, right: %s' % (left_neighbor, right_neighbor))

  if left_neighbor is not None:
    ln_parent = get(root, left_neighbor[:-1])
    ln_parent[left_neighbor[-1]] += a

  if right_neighbor is not None:
    rn_parent = get(root, right_neighbor[:-1])
    rn_parent[right_neighbor[-1]] += b

  parent = get(root, ptr[:-1])
  parent[ptr[-1]] = 0

def split(root, ptr):
  v = get(root, ptr)
  if not isinstance(v, int):
    raise Exception('invalid call to split')

  a = v // 2
  b = v - a

  parent = get(root, ptr[:-1])
  parent[ptr[-1]] = [a, b]

def get(root, ptr):
  result = root
  for i in ptr:
    result = result[i]
  return result

def is_explodable(root, ptr):
  v = get(root, ptr)
  if not isinstance(v, list):
    return False

  a, b = v
  if not isinstance(a, int) or not isinstance(b, int):
    return False

  return depth(ptr) >= 4

def is_splittable(root, ptr):
  v = get(root, ptr)
  return isinstance(v, int) and v >= 10

def reduce_num(root):
  while True:
    # first pass: do any explosions
    ptr = leftmost(root)
    any_exploded = False
    while ptr is not None:
      if is_explodable(root, ptr):
        explode(root, ptr)
        any_exploded = True

        # print('after explode:  %s' % (stringify(root),))
      ptr = next(root, ptr)

    # second pass: do any splits
    ptr = leftmost(root)
    any_split = False
    while ptr is not None:
      if is_splittable(root, ptr):
        split(root, ptr)
        any_split = True

        # print('after split:    %s' % (stringify(root),))

        # if the split created an explodable pair, we need to return to the exploding step
        # if this proves too slow, maybe explode inline here?
        if is_explodable(root, ptr):
          break
      ptr = next(root, ptr)

    if not any_exploded and not any_split:
      break

  return root

def add_nums(a, b):
  added = deepcopy([a, b])
  # print('after addition: %s' % (stringify(added),))
  reduced = reduce_num(added)
  # print('after reduce:   %s' % (stringify(reduced),))
  return reduced

def magnitude(num):
  if isinstance(num, list):
    a, b = num
    return 3 * magnitude(a) + 2 * magnitude(b)
  return num

def part1():
  nums = read_file()

  total = None
  for num in nums:
    if total is None:
      total = num
      continue

    total = add_nums(total, num)

  mag = magnitude(total)
  print(stringify(total))
  print(mag)

def part2():
  cur_max_magnitude = -1

  nums = read_file()

  for i in range(len(nums)):
    for j in range(len(nums)):
      if i == j:
        continue

      added = add_nums(nums[i], nums[j])
      mag = magnitude(added)
      cur_max_magnitude = max(mag, cur_max_magnitude)

  print(cur_max_magnitude)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()