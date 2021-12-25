# 12/21/2021
# https://adventofcode.com/2021/day/22

import sys
import re
from collections import deque

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    lines = f.read().strip().splitlines()

  regexp = re.compile("(on|off) x=([0-9-]+)\\.\\.([0-9-]+),y=([0-9-]+)\\.\\.([0-9-]+),z=([0-9-]+)\\.\\.([0-9-]+)")
  for line in lines:
    match = regexp.search(line)
    if match:
      nums = [int(match.group(i)) for i in range(2,8)]
      # Need to add 1 to upper bounds here since problem description is in
      # terms of inclusive points,
      # not exclusive ranges
      nums = tuple(n + (1 if i % 2 == 1 else 0) for i, n in enumerate(nums))
      on = match.group(1)
      yield on, nums

def is_initialization_cube(cube):
  x1, x2, y1, y2, z1, z2 = cube
  if x1 < -50 or y1 < -50 or z1 < -50:
    return False
  if x2 > 51 or y2 > 51 or z2 > 51:
    return False
  return True

def volume(cube):
  x1, x2, y1, y2, z1, z2 = cube
  vol = abs((x1 - x2) * (y1 - y2) * (z1 - z2))
  return vol

def subdivide_by_intersection(existing, new):
  intersection = intersect(existing, new)
  if intersection is None:
    return intersection, [existing]

  ex1, ex2, ey1, ey2, ez1, ez2 = existing
  ix1, ix2, iy1, iy2, iz1, iz2 = intersection

  remainder = []
  for x1, x2 in ((ex1, ix1), (ix1, ix2), (ix2, ex2)):
    if x1 == x2:
      continue
    for y1, y2 in ((ey1, iy1), (iy1, iy2), (iy2, ey2)):
      if y1 == y2:
        continue
      for z1, z2 in ((ez1, iz1), (iz1, iz2), (iz2, ez2)):
        if z1 == z2:
          continue

        cube = (x1, x2, y1, y2, z1, z2)
        if cube != intersection:
          remainder.append(cube)

  return intersection, remainder

def intersect(c1, c2):
  c1x1, c1x2, c1y1, c1y2, c1z1, c1z2 = c1
  c2x1, c2x2, c2y1, c2y2, c2z1, c2z2 = c2

  xi = intersect_1d(c1x1, c1x2, c2x1, c2x2)
  if xi is None:
    return None

  yi = intersect_1d(c1y1, c1y2, c2y1, c2y2)
  if yi is None:
    return None

  zi = intersect_1d(c1z1, c1z2, c2z1, c2z2)
  if zi is None:
    return None

  return xi + yi + zi

def intersect_1d(x1, x2, x3, x4):
  if max(x1, x2) <= min(x3, x4):
    return None
  elif min(x1, x2) >= max(x3, x4):
    return None
  return max(x1, x3), min(x2, x4)

def part1(should_filter=True):
  file_contents = read_file()
  augmented = [t + (i,) for i, t in enumerate(file_contents)]
  input_cubes = [c for c in augmented if not should_filter or is_initialization_cube(c[1])]

  on_cubes = []

  cubes_to_add = deque(input_cubes)
  while len(cubes_to_add) != 0:
    on, cube, input_idx = cubes_to_add.popleft()

    for i in range(len(on_cubes)-1,-1,-1):
      onc = on_cubes[i]
      intersection, remainder = subdivide_by_intersection(onc, cube)
      if intersection is None:
        continue

      _, inv_remainder = subdivide_by_intersection(cube, onc)

      if on == 'on':
        # ignore intersection, add the remainder of the new cube to the queue
        cubes_to_add.extendleft((on, c, input_idx + 0.001) for c in inv_remainder)
        break
      else:
        # replace the existing cube w/ remainder
        # re-add inv_remainder to queue
        on_cubes.pop(i)
        on_cubes.extend(remainder)
        cubes_to_add.extendleft((on, c, input_idx + 0.001) for c in inv_remainder)
        break
    else:
      # if we didn't break out of the loop, the new cube didn't intersect with
      # any existing cube. Just add to list
      if on == 'on':
        on_cubes.append(cube)

    # print("after line %.3f: %d" % (input_idx, sum(volume(c) for c in on_cubes)))

  total_on = sum(volume(c) for c in on_cubes)

  print(total_on)

def part2():
  part1(False)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
