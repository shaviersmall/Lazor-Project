import time
import numpy as np
import copy
import itertools

def read_BFF(file_name):
  grid = []
  lasers = []
  points = []
  # Each block has its own count
  blocks = {'A': 0, 'B': 0, 'C': 0}
  
  L_count = 0
  P_count = 0

  file = []
  with open(file_name, 'r') as f:
    lines = f.readlines()

  for line in lines:
    if line.startswith('GRID START'):
      while line.startswith('GRID STOP') == False:
        grid.append(line.strip())
    elif line.startswith('L '):
      # Laser has origin coordinates and directions
      x, y, dx, dy = map(int, line.split()[1:])
      lasers.append((x, y, dx, dy))
    elif line.startswith('P '):
      # Points have coordinates
      x, y = map(int, line.split()[1:])
            targets.append((x, y))
    elif line.startswith("A ") or line.startswith("B ") or line.startswith("C "):
      # Amount of blocks is equal to the number in the file.
      block_type, count = line.split()
      blocks[block_type] = int(count)
  return grid, lasers, targets, blocks
      


class play_game
