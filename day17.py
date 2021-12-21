# 12/20/2021
# https://adventofcode.com/2021/day/17

import sys
import re

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    text = f.read().strip()
    match = re.search("x=([0-9-]+)\\.\\.([0-9-]+), y=([0-9-]+)\\.\\.([0-9-]+)", text)
    if not match:
      raise Exception('invalid input')

    x1, x2, y1, y2 = [int(n) for n in match.group(1, 2, 3, 4)]
    return (x1, y1), (x2, y2)

# -1 if before the range, 0 if within the range, 1 if after the range
def range_compare(value, a, b):
  assert a <= b
  if value > b:
    return 1
  if value < a:
    return -1
  return 0

def y_update_fn(vy):
  return vy - 1

def x_update_fn(vx):
  if vx == 0:
    return 0

  if vx > 0:
    return vx - 1

  return vx + 1

def compute_y_trajectory(initial_vy, y1, y2, update_fn=y_update_fn):
  max_steps = 10000
  y = 0
  vy = initial_vy
  traj = []

  comp = range_compare(y, y1, y2)
  valid = False

  for step in range(max_steps):
    y += vy
    vy = update_fn(vy)
    traj.append(y)

    new_comp = range_compare(y, y1, y2)
    if new_comp == 0:
      # trajectory enters target
      # return True, traj
      valid = True
    elif new_comp != comp:
      # this trajectory does not enter the target at all
      break

  return valid, traj

def compute_x_trajectory(initial_vx, x1, x2):
  return compute_y_trajectory(initial_vx, x1, x2, x_update_fn)

def is_xy_traj_valid(x_traj, x1, x2, y_traj, y1, y2):
  x_set = set()
  for i, x in enumerate(x_traj):
    if range_compare(x, x1, x2) == 0:
      x_set.add(i)
  for i, y in enumerate(y_traj):
    if range_compare(y, y1, y2) == 0:
      if i in x_set:
        return True
  return False

def part1():
  (x1, y1), (x2, y2) = read_file()
  max_initial_vy = 1000

  max_y = 0
  vy_max = 0

  for initial_vy in range(-max_initial_vy, max_initial_vy):
    success, traj = compute_y_trajectory(initial_vy, y1, y2)

    traj_max = max(traj)
    if success and max_y < traj_max:
      max_y = traj_max
      vy_max = initial_vy

  print("max_y:%d from initial_vy:%d" % (max_y, vy_max))

def part2():
  (x1, y1), (x2, y2) = read_file()
  max_initial_vy = 1000
  max_initial_vx = 1000

  valid_y_trajs = []
  valid_x_trajs = []

  for initial_vy in range(-max_initial_vy, max_initial_vy):
    success, traj = compute_y_trajectory(initial_vy, y1, y2)
    if success:
      valid_y_trajs.append(traj)

  for initial_vx in range(-max_initial_vx, max_initial_vx):
    success, traj = compute_x_trajectory(initial_vx, x1, x2)
    if success:
      valid_x_trajs.append(traj)

  count = 0
  for y_traj in valid_y_trajs:
    for x_traj in valid_x_trajs:
      if is_xy_traj_valid(x_traj, x1, x2, y_traj, y1, y2):
        count += 1

  print(count)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()