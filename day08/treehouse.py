#!/usr/bin/env python3

import os
import sys

from typing import *

from functools import reduce

import numpy as np

def load_grid(input_file: str='input.txt') -> np.ndarray:
    with open(input_file, 'r') as fp:
        grid = [[*map(int, line.strip())] for line in fp.readlines()]

    return np.array(grid, dtype=np.uint64)

def count_visible(grid: np.ndarray) -> int:
    rows, columns = grid.shape
    visible = np.zeros_like(grid)

    # add perimeter visibility
    for row in range(0, rows, rows-1):
        visible[row, :] = 1
    for column in range(0, columns, columns-1):
        visible[:, column] = 1

    # from top/bottom
    for row in range(1, rows - 1):
        visible[row, :] |= (grid[row, :] > grid[:row, :].max(axis=0)) | (grid[row, :] > grid[row+1:, :].max(axis=0))
 
    # from left/right
    for column in range(1, columns - 1):
        visible[:, column] |= (grid[:, column] > grid[:, :column].max(axis=1)) | (grid[:, column] > grid[:, column+1:].max(axis=1))

    return visible.sum() 

# counting trailing zeros
def ctz(v: int) -> int:
    if v == 0:
        return 0

    return (-v & v).bit_length() - 1

def distance(bits: np.ndarray) -> int:
    # Horner's method on binary
    v = reduce(lambda a, b: (a << 1) | b, bits.tolist(), 1) # add leading one to count zeros properly

    return min(ctz(v) + 1, len(bits)) # don't count boundary condition outside of grid

def maximum_scenic_score(grid: np.ndarray) -> int:
    rows, columns = grid.shape
    score = np.ones_like(grid)

    # add perimeter scores
    for row in range(0, rows, rows-1):
        score[row, :] = 0
    for column in range(0, columns, columns-1):
        score[:, column] = 0

    # from left/right/top/bottom
    for row in range(1, rows - 1):
        for column in range(1, columns - 1):
            # indexing from edge to cell inward
            score[row, column] *= distance(grid[row, column] <= grid[row, +0:column:+1]) # left
            score[row, column] *= distance(grid[row, column] <= grid[row, -1:column:-1]) # right
            score[row, column] *= distance(grid[row, column] <= grid[+0:row:+1, column]) # top
            score[row, column] *= distance(grid[row, column] <= grid[-1:row:-1, column]) # bottom
 
    return score.max()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        grid = load_grid(sys.argv[1])
    else:
        grid = load_grid()

    print(f'Maximum count of trees visible:     {count_visible(grid)}')
    print(f'Maximum scenic score for treehouse: {maximum_scenic_score(grid)}')

