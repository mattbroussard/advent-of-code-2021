# 12/8/2021
# https://adventofcode.com/2021/day/4

import sys
from collections import deque

def mark_board(board, val):
  marked = False

  for row in board:
    for i, cell in enumerate(row):
      if cell == val:
        row[i] = None
        marked = True

  return marked

def is_winning(board):
  rows = len(board)
  cols = len(board[0])

  for row in board:
    found_val = False
    for v in row:
      if v is not None:
        found_val = True
        break

    if not found_val:
      return True

  for c in range(cols):
    found_val = False
    for r in range(rows):
      if board[r][c] is not None:
        found_val = True
        break

    if not found_val:
      return True

  return False

def score_board(board, last_call):
  total = 0
  for row in board:
    for cell in row:
      if cell is not None:
        total += cell

  return total * last_call

def part1():
  fname = sys.argv[1]

  calls = None
  boards = []

  with open(fname, 'r') as f:
    for line in f:
      if calls is None:
        calls = [int(n) for n in line.split(',')]
        continue

      if len(line.strip()) == 0:
        boards.append([])
        continue

      boards[-1].append([int(n) for n in line.split(" ") if len(n) > 0])

  for idx, call in enumerate(calls):
    for board in boards:
      marked = mark_board(board, call)
      if marked and is_winning(board):
        score = score_board(board, call)
        print(score)
        return

  print("No winner.")

def part2():
  fname = sys.argv[1]

  calls = None
  boards = []

  with open(fname, 'r') as f:
    for line in f:
      if calls is None:
        calls = [int(n) for n in line.split(',')]
        continue

      if len(line.strip()) == 0:
        boards.append([])
        continue

      boards[-1].append([int(n) for n in line.split(" ") if len(n) > 0])

  wins = []
  winning_calls = {}

  for idx, call in enumerate(calls):
    for board_idx, board in enumerate(boards):
      if board_idx in wins:
        continue

      marked = mark_board(board, call)
      if marked and is_winning(board):
        score = score_board(board, call)
        wins.append(board_idx)
        winning_calls[board_idx] = call

  if len(wins) == 0:
    print("No winner.")
    return

  last_board = boards[wins[-1]]
  last_call = winning_calls[wins[-1]]
  last_score = score_board(last_board, last_call)
  print(last_score)

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()