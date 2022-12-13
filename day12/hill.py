#!/usr/bin/env python3

import os
import sys

from typing import *
from numpy.typing import NDArray

from operator import sub
from math import hypot

from string import ascii_lowercase as letters

from heapdict import heapdict

import numpy as np

encode = {letter: index for index, letter in enumerate(letters)}

def load_contour(input_file: str='input.txt', encode: Dict[str, int]=encode) -> Tuple[NDArray[np.int64], Tuple[int, int], Tuple[int, int]]:
    with open(input_file, 'r') as fp:
        rows = [list(line.strip()) for line in fp.readlines()]

    contour = np.array(rows, dtype=np.str_)
    start = *map(int, np.where(contour == 'S')),
    end = *map(int, np.where(contour == 'E')),
    contour[start], contour[end] = 'a', 'z'
    contour = np.vectorize(lambda letter: encode[letter], otypes=[np.int64])(contour)

    return contour, start, end

# A* algorithm
def a_star(contour: NDArray[np.int64], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    def h(location: Tuple[int, int]) -> float:
        # heuristic estimate of "future" cost (cannot overestimate for admissibility)
        return hypot(*map(sub, location, end)) # Euclidean distance

    rows, columns = contour.shape

    f = np.full_like(contour, fill_value=np.inf, dtype=np.float64) 
    g = np.full_like(contour, fill_value=1_000_000_000, dtype=np.uint64) 

    f[start], g[start] = h(start), 0
    
    open = heapdict() # a minheap
    open[start] = f[start]

    while open:
        current, _ = open.popitem()
        row, column = current
        height = contour[row, column]

        if current == end:
            return g[current]

        for r, c in [(row+1, column), (row, column+1), (row-1, column), (row, column-1)]: # down, right, up, left
            # "the elevation of the neighbor square can be at most one higher than the elevation of your current square"
            if (r >= 0) and (r < rows) and (c >= 0) and (c < columns) and (contour[r, c] - height <= 1):
                neighbor = (r, c)
                g_new = g[current] + 1
                if g_new < g[neighbor]:
                    f[neighbor], g[neighbor] = g_new + h(neighbor), g_new
                    open[neighbor] = f[neighbor] # update key if present, add key if not

    return -1 # unreachable

def fewest_steps(contour: NDArray[np.int64], end: Tuple[int, int]) -> int:
    results = [a_star(contour, start, end) for start in map(tuple, np.transpose(np.where(contour == 0)))]
    
    return min(result for result in results if result > 0) # exclude unreachable starting positions


if __name__ == "__main__":
    if len(sys.argv) > 1:
        contour, start, end = load_contour(sys.argv[1])
    else:
        contour, start, end = load_contour()

    print(f'Fewest steps from start to end:  {a_star(contour, start, end)}')
    print(f'Fewest steps from bottom to end: {fewest_steps(contour, end)}')

