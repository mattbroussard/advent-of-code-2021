# 12/20/2021
# https://adventofcode.com/2021/day/20

import sys

def convert_grid_to_dict(rows):
  ret = {}

  for y, row in enumerate(rows):
    for x, c in enumerate(row):
      ret[(x, y)] = c

  dims = (0, 0, len(rows[0]), len(rows))

  return ret, dims

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    lines = f.read().splitlines()

    enhancer = lines[0].strip()
    image, dims = convert_grid_to_dict([l.strip() for l in lines[2:]])

    return enhancer, image, dims

def neighbor_coords(x, y):
  for dy in range(-1, 2):
    for dx in range(-1, 2):
      yield (x + dx, y + dy)

def get_enhancer_key(image, x, y, outer):
  key = 0
  for x, y in neighbor_coords(x, y):
    c = image.get((x, y), outer)
    b = 1 if c == '#' else 0
    key <<= 1
    key |= b
  return key

def enhance(enhancer, image, dims, outer='.'):
  new_outer = enhancer[0 if outer == '.' else -1]

  ox, oy, width, height = dims
  ox -= 1
  oy -= 1
  width += 2
  height += 2
  expanded_dims = (ox, oy, width, height)

  new_image = {}

  # debug
  # nc = list(neighbor_coords(1, 1))
  # ncs = "".join(image.get((x, y), outer) for x, y in nc)
  # ek = get_enhancer_key(image, 1, 1, outer)
  # e = enhancer[ek]
  # print("at (1,1): ek=%s, e=%s, ncs=%s, nc=%s" % (ek, e, ncs, nc))

  for y in range(oy, oy + height):
    for x in range(ox, ox + height):
      key = get_enhancer_key(image, x, y, outer)
      new_image[(x, y)] = enhancer[key]

  return new_image, expanded_dims, new_outer

def print_image(image, dims, outer):
  ox, oy, width, height = dims
  for y in range(oy, oy + height):
    s = "".join(image.get((x, y), outer) for x in range(ox, ox + width))
    print(s)

def part1(rounds=2):
  enhancer, image, dims = read_file()

  outer = '.'
  for _ in range(rounds):
    image, dims, outer = enhance(enhancer, image, dims, outer)
    # print_image(image, dims, outer)

  if outer == '#':
    return float('inf')

  count = sum(1 if c == '#' else 0 for c in image.values())
  return count

def part2():
  return part1(50)

def main():
  p1 = part1()
  print(p1)
  p2 = part2()
  print(p2)

if __name__ == '__main__':
  main()