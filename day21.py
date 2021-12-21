# 12/20/2021
# https://adventofcode.com/2021/day/21

import sys
from collections import defaultdict

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    lines = f.read().strip().splitlines()
    positions = [int(line.split(': ')[1]) for line in lines]
    return positions

class DeterministicDie:
  roll_count = 0

  def roll(self):
    ret = (self.roll_count % 100) + 1
    self.roll_count += 1
    return ret

def roll3(die):
  return sum(die.roll() for _ in range(3))

def part1(die=DeterministicDie()):
  positions = read_file()
  scores = [0] * len(positions)

  stop = False
  while True:
    if stop:
      break

    for player in range(len(positions)):
      rolled = roll3(die)
      positions[player] = ((positions[player] - 1 + rolled) % 10) + 1
      scores[player] += positions[player]

      if scores[player] >= 1000:
        stop = True
        break

  losing_score = min(scores)
  result = losing_score * die.roll_count

  print(result)

def compute_dirac_outcomes():
  freqs = defaultdict(lambda: 0)
  for i in range(1,4):
    for j in range(1,4):
      for k in range(1,4):
        freqs[i+j+k] += 1
  return list(freqs.items())

def update_univ(univ, player_idx, new_state):
  return tuple(new_state if i == player_idx else old_state for i, old_state in enumerate(univ))

def part2():
  init_positions = read_file()
  init_scores = [0] * len(init_positions)
  state = tuple(zip(init_positions, init_scores))

  univs = [(state, 1)]
  won_univ_counts = [0] * len(init_positions)

  dirac_outcomes = compute_dirac_outcomes()

  player_idx = 0
  generation_idx = 0
  while len(univs) > 0:
    next_univs = []
    for univ, count in univs:
      for rolled, freq in dirac_outcomes:
        pos, score = univ[player_idx]
        pos = ((pos - 1 + rolled) % 10) + 1
        score += pos

        if score >= 21:
          won_univ_counts[player_idx] += freq * count

          # debug
          # if generation_idx == 0:
          #   print("gen0 player0 won univ: %s" % ((pos, score),))
        else:
          next_univs.append((update_univ(univ, player_idx, (pos, score)), count * freq))

    # print("Generation %d (player %d): %d -> %d universes (%s won so far)" % (generation_idx, player_idx, len(univs), len(next_univs), won_univ_counts))
    # print(next_univs)

    univs = next_univs
    player_idx = (player_idx + 1) % len(init_positions)
    generation_idx += 1

    max_score = 0
    expanded_count = 0
    for univ, count in univs:
      for _, score in univ:
        max_score = max(max_score, score)
      expanded_count += count
    print("Generation %d: len(univs)=%d (%d expanded), won: %s, max_score=%d" % (generation_idx, len(univs), expanded_count, won_univ_counts, max_score))

  result = max(won_univ_counts)
  print(result)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()