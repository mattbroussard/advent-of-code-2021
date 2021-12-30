# 12/29/2021
# https://adventofcode.com/2021/day/23

from copy import deepcopy
import heapq
from collections import defaultdict, deque
from functools import cache

part1_empty_map = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#__
  #########__
"""[1:-1].replace("_", " ")

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

part1_super_easy = """
#############
#...........#
###B#A#C#D###
  #A#B#C#D#
  #########
"""[1:-1]

# Define which coordinates correspond to rooms and hall
p1_room1 = [(3, 2), (3, 3)]
p1_room2 = [(5, 2), (5, 3)]
p1_room3 = [(7, 2), (7, 3)]
p1_room4 = [(9, 2), (9, 3)]
p1_rooms_separate = [p1_room1, p1_room2, p1_room3, p1_room4]
p1_rooms = [pos for room in p1_rooms_separate for pos in room]
p1_rooms_set = set(p1_rooms)
p1_rooms_x = set(x for x, _ in p1_rooms)
p1_hall = [(x, 1) for x in range(1,12) if x not in p1_rooms_x]

# Constants related to other rules
per_move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
# per_move_costs = {k: 1 for k in 'ABCD'}

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

@cache
def pathfind_empty(src, dst, empty_map=part1_empty_map):
  lines = empty_map.splitlines()
  width = len(lines[0])
  height = len(lines)

  frontier = deque([(src,)])
  visited = set([src])
  neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

  while len(frontier) > 0:
    cur_path = frontier.popleft()
    cur = cur_path[-1]
    x, y = cur

    for dx, dy in neighbors:
      x2, y2 = x + dx, y + dy
      pt = (x2, y2)
      if x2 < 0 or x2 >= width or y2 < 0 or y2 >= height:
        continue
      if pt in visited:
        continue
      if lines[y2][x2] != '.':
        continue
      if pt == dst:
        return cur_path[1:] + (pt,)

      visited.add(pt)
      frontier.append(cur_path + (pt,))

  raise Exception("pathfind_empty couldn't find a route %s -> %s" % (src, dst))

keep_history = True

class State:
  # map: agent type -> list(tuple(coord, step_count))
  agent_states = None
  cost_so_far = 0
  # tuple: (agent_type, agent_idx)
  last_agent_to_move = None

  # only populated if keep_history==True
  prev_state = None

  # This constructor clones by default, then modifications can be made
  # subsequently by the caller
  def __init__(self, other=None):
    if other is not None:
      self.agent_states = deepcopy(other.agent_states)
      self.cost_so_far = other.cost_so_far
      if keep_history:
        self.prev_state = other

  def is_winning_p1(self):
    # map: agent type -> list(room num)
    room_assignments = defaultdict(list)

    for agent_type, states in self.agent_states.items():
      for i, (pos, steps) in enumerate(states):
        if steps > 2:
          raise Exception("ERROR: found an agent that has moved more than 2 times (%s%d)" % (agent_type, i))
          return False

        # Every agent must be in a room
        if pos not in p1_rooms_set:
          return False
        room_assignments[agent_type].append(p1_room_num(p1_rooms.index(pos)))

    for agent_type, expected_room in zip(sorted(room_assignments.keys()), range(len(room_assignments))):
      v = room_assignments[agent_type]
      # Agents must be arranged alphabetically from left to right
      if v[0] != expected_room:
        return False

      # Every room must contain just one type of agent
      if len(set(v)) != 1:
        return False

    return True

  def get_successors_p1(self):
    # assumption: already checked not winning before calling get_successors

    for agent_type, states in self.agent_states.items():
      for agent_idx, (pos, steps) in enumerate(states):
        # This agent can't move anymore
        if steps >= 2:
          continue

        # Same agent cannot move twice consecutively
        if self.last_agent_to_move == (agent_type, agent_idx):
          continue

        for next_pos in p1_transitions[pos]:
          # Can't backtrack from the direction that destination is in
          # TODO: not sure if this rule is actually correct?
          # if self.is_move_in_wrong_direction(pos, next_pos, agent_type):
          #   continue

          # Can't go someplace another agent is already
          if self.position_collides(next_pos):
            continue

          # If entering a room:
          #  - must go to bottom-most open slot
          #  - cannot enter a room that contains a different agent type
          #  - rooms must be arranged alphabetically
          if self.is_illegal_room_destination(next_pos, agent_type):
            continue

          # Path to the next space may not contain any other agent
          path = pathfind_empty(pos, next_pos, part1_empty_map)
          if self.path_collides(path):
            continue

          new_state = State(self)
          new_state.agent_states[agent_type][agent_idx] = (next_pos, steps + 1)
          new_state.cost_so_far += len(path) * per_move_costs[agent_type]
          new_state.last_agent_to_move = (agent_type, agent_idx)
          yield new_state

  def agent_at(self, pos):
    for agent_type, states in self.agent_states.items():
      for i, (coord, _) in enumerate(states):
        if pos == coord:
          return (agent_type, i)
    return None

  def position_collides(self, pos):
    return self.agent_at(pos) is not None

  def path_collides(self, path):
    for pos in path:
      if self.position_collides(pos):
        return True
    return False

  def expected_room_for_agent_type(self, agent_type):
    return sorted(self.agent_states.keys()).index(agent_type)

  def is_illegal_room_destination(self, pos, agent_type):
    if pos not in p1_rooms_set:
      return False

    expected_room = self.expected_room_for_agent_type(agent_type)

    for room_idx, room in enumerate(p1_rooms_separate):
      if pos not in room:
        continue

      # Agents must be arranged alphabetically into the rooms
      if room_idx != expected_room:
        return True

      best_open_idx = max(range(len(room)), key=lambda i: i if not self.position_collides(room[i]) else -100)
      if best_open_idx >= 0:
        # If a different agent type is already in this room, don't let this one enter
        if best_open_idx < len(room) - 1:
          first_into_room_agent_type, _ = self.agent_at(room[-1])
          if first_into_room_agent_type != agent_type:
            return True

        # Don't enter a room without going all the way in
        return pos != room[best_open_idx]

      break

    # This probably means this method was called on a room pos that's already full?
    raise Exception("is_illegal_room_destination invalid state: pos=%s" % (pos,))
    return False

  # This rule sped things up a lot, but turned out to be wrong and gives wrong answer for part 1 puzzle input.
  # def is_move_in_wrong_direction(self, pos, next_pos, agent_type):
  #   expected_room = self.expected_room_for_agent_type(agent_type)
  #   expected_x = p1_rooms_separate[expected_room][0][0]

  #   # entering desired room
  #   if expected_x == next_pos[0]:
  #     return False

  #   # Technically, this means leaving the column we will eventually be in and would be "backtracking",
  #   # but we allow it here because:
  #   #  1) it would cause div-by-0 below
  #   #  2) might need to temporarily move out of the way to let a different agent under you get out
  #   if expected_x == pos[0]:
  #     return False

  #   expected_dir = expected_x - pos[0]
  #   expected_dir /= abs(expected_dir)

  #   actual_dir = next_pos[0] - pos[0]
  #   actual_dir /= abs(actual_dir)

  #   return expected_dir != actual_dir

  def __lt__(self, other):
    return self.cost_so_far < other.cost_so_far

  def hash_tuple(self):
    # prev_state pointer intentionally not part of hash_tuple
    ht = (self.cost_so_far, self.last_agent_to_move)
    for key in sorted(self.agent_states.keys()):
      for agent_state in self.agent_states[key]:
        ht += (agent_state,)
    return ht

  def __eq__(self, other):
    return isinstance(other, State) and self.hash_tuple() == other.hash_tuple()

  def __hash__(self):
    return hash(self.hash_tuple())

  def __str__(self):
    lines = [list(line) for line in part1_empty_map.splitlines()]
    for agent_type, states in self.agent_states.items():
      for (x, y), _ in states:
        lines[y][x] = agent_type

    stat_lines = [
      "  total cost: %d" % (self.cost_so_far)
    ] + [
      "  " + "  ".join(
        "%s%s%s: %d" % (
          "*" if (agent_type, i) == self.last_agent_to_move else " ",
          agent_type,
          i,
          steps
        )
        for i, (_, steps) in enumerate(self.agent_states[agent_type])
      )
      for agent_type in sorted(self.agent_states.keys())
    ]

    lines = ["".join(line) for line in lines]
    return "\n".join((a or "") + (b or "") for a,b in zip(lines, stat_lines))

  def get_full_history(self):
    cur = self
    history = []
    while cur is not None:
      history.append(cur)
      cur = cur.prev_state
    history.reverse()
    return history

def input_str_to_initial_state(input_str):
  agents = defaultdict(list)

  lines = input_str.splitlines()
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      if c in 'ABCD':
        agents[c].append(((x, y), 0))

  state = State()
  state.agent_states = dict(agents)
  return state

def part1(input_str):
  initial_state = input_str_to_initial_state(input_str)

  frontier = [(initial_state.cost_so_far, initial_state)]
  visited = set([initial_state])
  iterations = 0
  while len(frontier) > 0:
    iterations += 1
    _, cur = heapq.heappop(frontier)

    if cur.is_winning_p1():
      win_history = cur.get_full_history()
      print("Winning strategy (%d steps):" % (len(win_history)))
      for state in win_history:
        print(str(state))

      return cur.cost_so_far

    # This method will handle filtering for valid successors only.
    # It is also defined such that no cycles are possible, though separately
    # reached and equivalent states are possible so we still keep a visited set
    for successor in cur.get_successors_p1():
      if successor not in visited:
        visited.add(successor)
        heapq.heappush(frontier, (successor.cost_so_far, successor))

    if iterations % 1000 == 0:
      print("Iteration %6d, %7d entries in frontier" % (iterations, len(frontier)))
      print(str(frontier[0][1]))

  print("Error: exhausted graph without finding win condition")
  return -1

def main():
  p1_result = part1(part1_puzzle_map)
  print("Part 1 result: %d" % (p1_result,))

if __name__ == '__main__':
  main()
