#!/usr/bin/env python3

import os
import sys

from typing import *
from numpy.typing import NDArray

from more_itertools import windowed

import re

import numpy as np
def load_cave(input_file: str='input.txt', floor: bool=False, sand_coordinate: Tuple[int, int]=(500, 0), vein_pattern: re.Pattern=re.compile(r'(\d+),(\d+)')) -> Tuple[NDArray[np.bool_], int]:
    def line(start: int, end: int) -> slice:
        if start > end:
            start, end = end, start
        return slice(start, end+1, 1)

    with open(input_file, 'r') as fp:
        lines = [line.strip() for line in fp.readlines()]

    veins = [[tuple(int(coordinate) for coordinate in coordinates) for coordinates in vein_pattern.findall(line)] for line in lines]

    endpoints = np.array([[ordinate, abscissa] for vein in veins for abscissa, ordinate in vein])

    maximum = endpoints.max(axis=0)
    minimum = np.append([0], endpoints[:, 1].min(axis=0))
    if floor: # i.e. if not abyss
        # shape of sandpile is 45°-45°-90° triangle with right angle at "spigot" (i.e. w = 2*h)
        maximum[0] += 2 # floor has y coordinate equal to two plus max y
        minimum[1] = min(minimum[1], sand_coordinate[0] - maximum[0])
        maximum[1] = max(maximum[1], sand_coordinate[0] + maximum[0])
        floor_vein = [(minimum[1], maximum[0]), (maximum[1], maximum[0])]
        veins.append(floor_vein)

    column_offset = -minimum[1]
    shape = maximum - minimum + 1
    cave = np.zeros(shape, dtype=np.bool_)

    for vein in veins:
        for (c1, r1), (c2, r2) in windowed(vein, 2):
            cave[line(r1, r2), line(c1+column_offset, c2+column_offset)] |= True

    return cave, column_offset

def simulate(cave: NDArray[np.bool_], column_offset: int, sand_coordinate: Tuple[int, int]=(500, 0)) -> NDArray[np.bool_]:
    sr, sc = sand_coordinate[1], sand_coordinate[0]+column_offset

    blocked = cave.copy()
    rows, columns = blocked.shape

    abyss = False
    while not abyss and not blocked[sr, sc]:
        abyss = True
        c = sc
        for r in range(sr, rows-1):
            if not blocked[r+1, c]:
                continue # keep falling
            elif not blocked[r+1, c-1]:
                c -= 1 # keep falling diagonally to the left
                continue
            elif not blocked[r+1, c+1]:
                c += 1 # keep falling diagonally to the right
                continue
            blocked[r, c] = True
            abyss = False
            break

    return blocked

legend = {
    -1: '+',
    0: '.',
    1: 'o',
    2: '#'
}

def render(cave: NDArray[np.bool_], blocked: Union[NDArray[np.bool_], None]=None, sand_coordinate: Tuple[int, int]=(500, 0), legend: Dict[int, str]=legend) -> None:
    sr, sc = sand_coordinate[1], sand_coordinate[0]+column_offset

    if blocked is None:
        composite = cave << 1
        composite[sr, sc] = -1 # render "spigot"
    else:
        composite = cave.astype(np.int64) + blocked.astype(np.int64)
        if not blocked[sr, sc]:
            composite[sr, sc] = -1 # render "spigot"

    for values in composite:
        for value in values:
            print(legend[value], end=' ')
        print('\n')

def count_sand(cave: NDArray[np.bool_], blocked: NDArray[np.bool_]) -> int:
    return np.count_nonzero(cave ^ blocked)



if __name__ == "__main__":
    kind = {True: 'floor', False: 'abyss'}
    for floor in [False, True]:
        if len(sys.argv) > 1:
            cave, column_offset = load_cave(sys.argv[1], floor=floor)
        else:
            cave, column_offset = load_cave(floor=floor)

        blocked = simulate(cave, column_offset)
        sand_count = count_sand(cave, blocked)

        print(f'Sand count with {kind[floor]}:  {sand_count}')

