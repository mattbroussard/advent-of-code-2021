# 12/12/2021
# https://adventofcode.com/2021/day/12

import sys
from collections import defaultdict, deque

def read_input():
  fname = sys.argv[1]

  edge_map = defaultdict(lambda: [])

  with open(fname, 'r') as f:
    for line in f:
      a, b = line.strip().split("-")
      edge_map[a].append(b)
      edge_map[b].append(a)

  return edge_map

def is_big(node):
  return node == node.upper()

def part1():
  graph = read_input()

  paths = set()
  frontier = deque()

  frontier.append(('start',))
  while len(frontier) > 0:
    path_so_far = frontier.popleft()
    cur_node = path_so_far[-1]

    for neighbor in graph[cur_node]:
      if neighbor in path_so_far and not is_big(neighbor):
        continue

      new_path = path_so_far + (neighbor,)
      if neighbor == 'end':
        paths.add(new_path)
        continue

      frontier.append(new_path)

  print(len(paths))

def has_any_small_dupe(path):
  seen = set()

  for n in path:
    if is_big(n):
      continue

    if n in seen:
      return True

    seen.add(n)

  return False

def part2():
  graph = read_input()

  paths = set()
  frontier = deque()

  frontier.append(('start',))
  while len(frontier) > 0:
    path_so_far = frontier.popleft()
    cur_node = path_so_far[-1]

    for neighbor in graph[cur_node]:
      if neighbor == 'start':
        continue

      if neighbor in path_so_far and not is_big(neighbor):
        if has_any_small_dupe(path_so_far):
          continue

      new_path = path_so_far + (neighbor,)
      if neighbor == 'end':
        paths.add(new_path)
        continue

      frontier.append(new_path)

  print(len(paths))

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
