# 12/29/2021
# https://adventofcode.com/2021/day/23

from copy import deepcopy
import heapq
from collections import defaultdict, deque
from functools import cache
import sys
from itertools import zip_longest

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

part2_empty_map = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#__
  #.#.#.#.#__
  #.#.#.#.#__
  #########__
"""[1:-1].replace("_", " ")

part2_sample_map = """
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
"""[1:-1]

part2_puzzle_map = """
#############
#...........#
###D#D#C#C###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#B#A#
  #########
"""[1:-1]

part2_super_easy = """
#############
#...........#
###B#A#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""[1:-1]

# Define which coordinates correspond to rooms and hall
p2_room1 = [(3, 2), (3, 3), (3, 4), (3, 5)]
p1_room1 = p2_room1[:2]
p2_room2 = [(5, 2), (5, 3), (5, 4), (5, 5)]
p1_room2 = p2_room2[:2]
p2_room3 = [(7, 2), (7, 3), (7, 4), (7, 5)]
p1_room3 = p2_room3[:2]
p2_room4 = [(9, 2), (9, 3), (9, 4), (9, 5)]
p1_room4 = p2_room4[:2]
p1_rooms_separate = [p1_room1, p1_room2, p1_room3, p1_room4]
p2_rooms_separate = [p2_room1, p2_room2, p2_room3, p2_room4]
p1_rooms = [pos for room in p1_rooms_separate for pos in room]
p2_rooms = [pos for room in p2_rooms_separate for pos in room]
p1_rooms_set = set(p1_rooms)
p2_rooms_set = set(p2_rooms)
p1_rooms_x = [3, 5, 7, 9]
p1_hall = [(x, 1) for x in range(1,12) if x not in p1_rooms_x]

# Constants related to other rules
per_move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def p1_room_num(idx_into_p1_rooms):
  return idx_into_p1_rooms // len(p1_room1)

def p2_room_num(idx_into_p2_rooms):
  return idx_into_p2_rooms // len(p2_room1)

# Define possible transitions between different positions
p1_transitions = defaultdict(list)
p2_transitions = defaultdict(list)
for h in p1_hall:
  p1_transitions[h] += p1_rooms
  p2_transitions[h] += p2_rooms
for i, r in enumerate(p1_rooms):
  p1_transitions[r] += p1_hall
  for j in range(len(p1_rooms)):
    if p1_room_num(i) != p1_room_num(j):
      p1_transitions[r].append(p1_rooms[j])
for i, r in enumerate(p2_rooms):
  p2_transitions[r] += p1_hall
  for j in range(len(p2_rooms)):
    if p2_room_num(i) != p2_room_num(j):
      p2_transitions[r].append(p2_rooms[j])

class PuzzleParams:
  def __init__(self, empty_map):
    self.rooms_x = p1_rooms_x
    self.hall = p1_hall
    self.per_move_costs = per_move_costs
    self.empty_map = empty_map

    if empty_map == part1_empty_map:
      self.room1 = p1_room1
      self.room2 = p1_room2
      self.room3 = p1_room3
      self.room4 = p1_room4
      self.rooms_separate = p1_rooms_separate
      self.rooms = p1_rooms
      self.rooms_set = p1_rooms_set
      self.transitions = p1_transitions
    elif empty_map == part2_empty_map:
      self.room1 = p2_room1
      self.room2 = p2_room2
      self.room3 = p2_room3
      self.room4 = p2_room4
      self.rooms_separate = p2_rooms_separate
      self.rooms = p2_rooms
      self.rooms_set = p2_rooms_set
      self.transitions = p2_transitions
    else:
      raise Exception('invalid input to PuzzleParams')

  def room_num(self, idx_into_rooms):
    if self.empty_map == part1_empty_map:
      return p1_room_num(idx_into_rooms)
    else:
      return p2_room_num(idx_into_rooms)

@cache
def pathfind_empty(src, dst, empty_map):
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

keep_history = False

class State:
  __slots__ = ("agent_states", "cost_so_far", "last_agent_to_move", "prev_state", "params")

  # map: agent type -> list(tuple(coord, step_count))
  # agent_states = None
  # cost_so_far = 0

  # tuple: (agent_type, agent_idx)
  # last_agent_to_move = None

  # only populated if keep_history==True
  # prev_state = None

  # params = None

  # This constructor clones by default, then modifications can be made
  # subsequently by the caller
  def __init__(self, other=None):
    # Must do this default init in __init__, not as class variables, when using __slots__
    # https://stackoverflow.com/a/41893938
    self.agent_states = None
    self.cost_so_far = 0
    self.last_agent_to_move = None
    self.prev_state = None
    self.params = None

    if other is not None:
      self.agent_states = deepcopy(other.agent_states)
      self.cost_so_far = other.cost_so_far
      self.params = other.params
      if keep_history:
        self.prev_state = other

  def is_winning(self):
    # map: agent type -> list(room num)
    room_assignments = defaultdict(list)

    for agent_type, states in self.agent_states.items():
      for i, (pos, steps) in enumerate(states):
        if steps > 2:
          raise Exception("ERROR: found an agent that has moved more than 2 times (%s%d)" % (agent_type, i))
          return False

        # Every agent must be in a room
        if pos not in self.params.rooms_set:
          return False
        room_assignments[agent_type].append(self.params.room_num(self.params.rooms.index(pos)))

    for agent_type, expected_room in zip(sorted(room_assignments.keys()), range(len(room_assignments))):
      v = room_assignments[agent_type]
      # Agents must be arranged alphabetically from left to right
      if v[0] != expected_room:
        return False

      # Every room must contain just one type of agent
      if len(set(v)) != 1:
        return False

    return True

  def get_successors(self):
    # assumption: already checked not winning before calling get_successors

    for agent_type, states in self.agent_states.items():
      for agent_idx, (pos, steps) in enumerate(states):
        # This agent can't move anymore
        if steps >= 2:
          continue

        # Same agent cannot move twice consecutively
        if self.last_agent_to_move == (agent_type, agent_idx):
          continue

        # ideal_hall_positions = self.compute_ideal_hall_positions(agent_type)

        for next_pos in self.params.transitions[pos]:
          # Can't backtrack from the direction that destination is in
          # TODO: not sure if this rule is actually correct?
          # if self.is_move_in_wrong_direction(pos, next_pos, agent_type):
          #   continue

          # Can't go someplace another agent is already
          if self.position_collides(next_pos):
            continue

          # If going to the hall, must go to an "ideal hall position" -- closest
          # open slots to final destination room
          # if next_pos not in self.params.rooms_set and next_pos not in ideal_hall_positions:
          #   continue

          # If entering a room:
          #  - must go to bottom-most open slot
          #  - cannot enter a room that contains a different agent type
          #  - rooms must be arranged alphabetically
          if self.is_illegal_room_destination(next_pos, agent_type):
            continue

          # Path to the next space may not contain any other agent
          path = pathfind_empty(pos, next_pos, self.params.empty_map)
          if self.path_collides(path):
            continue

          new_state = State(self)
          new_state.agent_states[agent_type][agent_idx] = (next_pos, steps + 1)
          new_state.cost_so_far += len(path) * per_move_costs[agent_type]
          new_state.last_agent_to_move = (agent_type, agent_idx)
          yield new_state

  def get_successors_v2(self):
    room_contents = [
      [x for x in [self.agent_at(pos) for pos in reversed(room)] if x is not None]
      for room in self.params.rooms_separate
    ]

    # Step 1: Try to move agent from front of each room out, if room needs any
    # changes
    for room_num, room in enumerate(room_contents):
      expected_agent = 'ABCD'[room_num]
      any_to_move = any(agent_type != expected_agent for agent_type, _ in room)
      if not any_to_move:
        continue

      front_of_room = self.params.rooms_separate[room_num][0]
      accessible_hall_slots = list(filter(
        lambda pos: \
          not self.position_collides(pos) and \
          not self.path_collides(pathfind_empty(front_of_room, pos, self.params.empty_map)),
        self.params.hall
      ))

      leader_type, leader_idx = room[-1]
      leader_pos = self.agent_states[leader_type][leader_idx][0]
      _, old_steps = self.agent_states[leader_type][leader_idx]
      if old_steps != 0:
        raise Exception('gs_v2: room %d leader %s%s has more than 0 steps already: %s' % (room_num, leader_type, leader_idx, self))

      for dest in accessible_hall_slots:
        path = pathfind_empty(leader_pos, dest, self.params.empty_map)
        cost = len(path) * per_move_costs[leader_type]

        new_state = State(self)
        new_state.agent_states[leader_type][leader_idx] = (dest, old_steps + 1)
        new_state.cost_so_far += cost
        yield new_state

    # Step 2: Try to move any agents in hallway into their final positions
    for hall_pos in self.params.hall:
      agent = self.agent_at(hall_pos)
      if agent is None:
        continue
      agent_type, agent_idx = agent
      agent_pos, agent_steps = self.agent_states[agent_type][agent_idx]
      if agent_steps != 1:
        raise Exception('gs_v2: agent %s%s in hall has wrong number of steps (%s): %s' % (agent_type, agent_idx, agent_steps, self))

      room_num = self.expected_room_for_agent_type(agent_type)
      room = room_contents[room_num]
      any_to_move = any(room_agent_type != agent_type for room_agent_type, _ in room)
      if any_to_move:
        continue

      dest = self.params.rooms_separate[room_num][-1 - len(room)]
      path = pathfind_empty(agent_pos, dest, self.params.empty_map)
      if self.path_collides(path):
        continue

      cost = len(path) * per_move_costs[agent_type]
      new_state = State(self)
      new_state.cost_so_far += cost
      new_state.agent_states[agent_type][agent_idx] = (dest, agent_steps + 1)
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

  # This gave exhausted search space without a solution :(
  # def compute_ideal_hall_positions(self, agent_type):
  #   desired_x = self.params.rooms_x[self.expected_room_for_agent_type(agent_type)]
  #   positions = {pos: abs(pos[0] - desired_x) for pos in self.params.hall if not self.position_collides(pos)}
  #   min_dist = min(positions.values())
  #   return [pos for pos, dist in positions.items() if dist == min_dist]

  def expected_room_for_agent_type(self, agent_type):
    return sorted(self.agent_states.keys()).index(agent_type)

  def is_illegal_room_destination(self, pos, agent_type):
    if pos not in self.params.rooms_set:
      return False

    expected_room = self.expected_room_for_agent_type(agent_type)

    for room_idx, room in enumerate(self.params.rooms_separate):
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
  #   expected_x = self.params.rooms_separate[expected_room][0][0]

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
    # prev_state pointer and params intentionally not part of hash_tuple
    ht = (self.cost_so_far, self.last_agent_to_move)
    for key in sorted(self.agent_states.keys()):
      for agent_state in self.agent_states[key]:
        ht += (agent_state,)
    return ht

  def __eq__(self, other):
    return isinstance(other, State) and self.hash_tuple() == other.hash_tuple()

  def __hash__(self):
    return hash(self.hash_tuple())

  def get_map_string(self):
    lines = [list(line) for line in self.params.empty_map.splitlines()]
    for agent_type, states in self.agent_states.items():
      for (x, y), _ in states:
        lines[y][x] = agent_type
    return "\n".join("".join(line) for line in lines)

  def __str__(self):
    lines = [list(line) for line in self.params.empty_map.splitlines()]
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
    return "\n" + "\n".join(a+b for a,b in zip_longest(lines, stat_lines, fillvalue=""))

  def __repr__(self):
    return self.__str__()

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
  is_part2 = len(lines) == 7
  empty = part2_empty_map if is_part2 else part1_empty_map

  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      if c in 'ABCD':
        agents[c].append(((x, y), 0))

  state = State()
  state.agent_states = dict(agents)
  state.params = PuzzleParams(empty)
  return state

def solve(input_str):
  initial_state = input_str_to_initial_state(input_str)

  frontier = [(initial_state.cost_so_far, initial_state)]
  visited = {initial_state.get_map_string(): 0}
  iterations = 0
  while len(frontier) > 0:
    iterations += 1
    _, cur = heapq.heappop(frontier)

    if cur.is_winning():
      win_history = cur.get_full_history()
      print("Winning strategy (%d steps):" % (len(win_history)))
      for state in win_history:
        print(str(state))

      return cur.cost_so_far

    # This method will handle filtering for valid successors only.
    # It is also defined such that no cycles are possible, though separately
    # reached and equivalent states are possible so we still keep a visited set
    successors = list(cur.get_successors_v2())
    # successors_old = list(cur.get_successors())

    # # debug
    # if set(successors) != set(successors_old):
    #   print('ERROR: v1 and v2 successor functions mismatch')
    #   print(successors)
    #   print('----------------------------------------------')
    #   print(successors_old)

    for successor in successors:
      ms = successor.get_map_string()
      if ms not in visited or visited[ms] > successor.cost_so_far:
        visited[ms] = successor.cost_so_far
        heapq.heappush(frontier, (successor.cost_so_far, successor))

    if iterations % 1000 == 0:
      print("Iteration %6d, %7d entries in frontier" % (iterations, len(frontier)))
      print(str(frontier[0][1]))

  print("Error: exhausted graph without finding win condition")
  return -1

def main():
  map_name = sys.argv[1] if len(sys.argv) >= 2 else None
  known_maps = {
    "part1_sample_map": part1_sample_map,
    "part1_puzzle_map": part1_puzzle_map,
    "part1_super_easy": part1_super_easy,
    "part2_sample_map": part2_sample_map,
    "part2_puzzle_map": part2_puzzle_map,
    "part2_super_easy": part2_super_easy,
  }

  map_to_solve = None
  if map_name is not None and map_name in known_maps:
    map_to_solve = known_maps[map_name]
    print("Solving map %s" % (map_name,))
  else:
    default_map = 'part2_puzzle_map'
    map_to_solve = known_maps[default_map]
    print("Unknown map name %s, defaulting to %s" % (map_name, default_map))

  result = solve(map_to_solve)
  print("Result: %d" % (result,))

if __name__ == '__main__':
  main()
