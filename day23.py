# 12/29/2021
# https://adventofcode.com/2021/day/23

from copy import deepcopy
import heapq
from collections import defaultdict

part1_empty_map = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #########
"""[1:-1]

part1_sample_map = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""[1:-1]

part1_puzzle_map = """
#############
#...........#
###D#D#C#C###
  #B#A#B#A#
  #########
"""[1:-1]

# Define which coordinates correspond to rooms and hall
p1_room1 = [(3, 2), (3, 3)]
p1_room2 = [(5, 2), (5, 3)]
p1_room3 = [(7, 2), (7, 3)]
p1_room4 = [(9, 2), (9, 3)]
p1_rooms = p1_room1 + p1_room2 + p1_room3 + p1_room4
p1_rooms_x = set(x for x, _ in p1_rooms)
p1_hall = [(x, 1) for x in range(1,12) if x not in p1_rooms_x]

def p1_room_num(idx_into_p1_rooms):
  return idx_into_p1_rooms // len(p1_room1)

# Define possible transitions between different positions
p1_transitions = defaultdict(list)
for h in p1_hall:
  p1_transitions[h] += p1_rooms
for i, r in enumerate(p1_rooms):
  p1_transitions[r] += p1_hall
  for j in range(len(p1_rooms)):
    if p1_room_num(i) != p1_room_num(j):
      p1_transitions[r].append(p1_rooms[j])

class State:
  # map: agent type -> list(tuple(coord, step_count))
  agent_states = None
  cost_so_far = 0

  # This constructor clones by default, then modifications can be made
  # subsequently by the caller
  def __init__(self, other=None):
    if other is not None:
      self.agent_states = deepcopy(other.agent_states)
      self.cost_so_far = other.cost_so_far

  def is_winning_p1(self):
    return False

  def get_successors_p1(self):
    return []

  def __lt__(self, other):
    return self.cost_so_far < other.cost_so_far

  def hash_tuple(self):
    ht = (self.cost_so_far,)
    for key in sorted(self.agent_states.keys()):
      for agent_state in self.agent_states[key]:
        ht += (agent_state,)
    return ht

  def __eq__(self, other):
    return isinstance(other, State) and self.hash_tuple() == other.hash_tuple()

  def __hash__(self):
    return hash(self.hash_tuple())

def input_str_to_initial_state(input_str):
  agents = defaultdict(list)

  lines = input_str.splitlines()
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      if c in 'ABCD':
        agents[c] += ((x, y), 0)

  state = State()
  state.agent_states = dict(agents)
  return state

def part1(input_str):
  initial_state = input_str_to_initial_state(input_str)

  frontier = [(initial_state.cost_so_far, initial_state)]
  visited = set([initial_state])
  while len(frontier) > 0:
    _, cur = heapq.heappop(frontier)

    if cur.is_winning_p1():
      return cur.cost_so_far

    # This method will handle filtering for valid successors only.
    # It is also defined such that no cycles are possible, though separately
    # reached and equivalent states are possible so we still keep a visited set
    for successor in cur.get_successors_p1():
      if successor not in visited:
        visited.add(successor)
        heapq.heappush(frontier, (successor.cost_so_far, successor))

  print("Error: exhausted graph without finding win condition")
  return -1


def main():
  p1_result = part1(part1_sample_map)
  print("Part 1 result: %d" % (p1_result,))

if __name__ == '__main__':
  main()
