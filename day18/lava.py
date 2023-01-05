#!/usr/bin/env python3

import os
import sys

from typing import *
from numpy.typing import NDArray

from operator import and_

from more_itertools import windowed

from collections import deque

import numpy as np
import pandas as pd

def load_cubes(input_file: str='input.txt') -> NDArray[np.bool_]:
    df = pd.read_csv(input_file, header=None, names=['x', 'y', 'z'])
    lattice = np.zeros(df.max() + 1, dtype=np.bool_)

    for _, (x, y, z) in df.iterrows():
        lattice[x, y, z] = True

    return lattice

def bubble_mask(lattice: NDArray[np.bool_]) -> NDArray[np.bool_]:
    rows, columns, layers = lattice.shape

    visited = lattice.copy() # treat lava as unnecessary to visit

    def neighbors(r: int, c: int, l: int) -> List[Tuple[int, int, int]]:
        return [(r + dr, c + dc, l + dl) for dr, dc, dl
                in [(-1, 0, 0), (+1, 0, 0), (0, -1, 0), (0, +1, 0), (0, 0, -1), (0, 0, +1)]
                if r + dr >= 0 and r + dr < rows
                and c + dc >= 0 and c + dc < columns
                and l + dl >= 0 and l + dl < layers
                and not visited[r + dr, c + dc, l + dl]
                ]

    def bfs(i: int, j: int, k: int):
        if not visited[i, j, k]:
            visited[i, j, k] = True
            queue: Deque[Tuple[int, int, int]] = deque([(i, j, k)])

            while queue:
                i, j, k = queue.popleft()
                for r, c, l in neighbors(i, j, k): # handles already visited
                    visited[r, c, l] = True
                    queue.append((r, c, l))

    # check connectivity from lattice surface
    # check top and bottom rows
    for i in [0, rows - 1]:
        for j in range(columns):
            for k in range(layers):
                bfs(i, j, k)

    # check left and right columns
    for j in [0, columns - 1]:
        for k in range(layers):
            for i in range(rows):
                bfs(i, j, k)

    # check front and back layers
    for k in [0, layers - 1]:
        for i in range(rows):
            for j in range(columns):
                bfs(i, j, k)

    return ~visited # i.e. the "bubbles"

def surface_area(lattice: NDArray[np.bool_], exterior: bool=False) -> int:
    if exterior:
        lattice |= bubble_mask(lattice)

    n = len(lattice.shape)
    count = 2*n*np.count_nonzero(lattice) # naive number of faces
    for dimension in range(n):
        for row in np.moveaxis(lattice, dimension, -1):
            for column in row:
                for pair in windowed(column, 2):
                    count -= 2*and_(*pair) # correct for internal faces

    return count


if __name__ == "__main__":
    if len(sys.argv) > 1:
        lattice = load_cubes(sys.argv[1])
    else:
        lattice = load_cubes()

    print(f'Total surface area of lava droplets, ignoring bubbles:      {surface_area(lattice)}')
    print(f'Exterior surface area of lava droplets, excluding bubbles:  {surface_area(lattice, exterior=True)}')

