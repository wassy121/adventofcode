#!/usr/bin/env python3

import os
import sys

from typing import *

from more_itertools import windowed

from operator import add, sub 
from math import hypot

def load_vectors(input_file: str='input.txt') -> List[Tuple[str, int]]:
    with open(input_file, 'r') as fp:
        return [(direction, int(magnitude)) for direction, magnitude in [line.strip().split() for line in fp.readlines()]]

movements: Dict[str, Tuple[int, int]] = {
    'L':  (-1, +0), # left
    'R':  (+1, +0), # right
    'U':  (+0, +1), # up
    'D':  (+0, -1)  # down
}

def step(direction: str, knots: List[Tuple[int, int]], movements: Dict[str, Tuple[int, int]]=movements) -> List[Tuple[int, int]]:
    def is_touching(head: Tuple[int, int], tail: Tuple[int, int]) -> bool:
        return hypot(*map(sub, head, tail)) < 1.5 # i.e. touching if Euclidean distance (i.e. hypotenuse ≤ √2 < 1.5 < √3 < 2)

    def signum(integer: int) -> int:
        return (integer > 0) - (integer < 0)

    def signed_sub(minuend: int, subtrahend: int) -> int:
        return signum(minuend - subtrahend)

    length = len(knots)

    # move head
    knots[0] = *map(add, knots[0], movements[direction]),

    for i, j in windowed(range(length), 2):
        #first, second = knots[i], knots[j]

        if is_touching(knots[i], knots[j]):
            # stay in place, don't move anything else
            break
        else:
            movement = *map(signed_sub, knots[i], knots[j]),
            knots[j] = *map(add, knots[j], movement),

    return knots

def steps(direction: str, magnitude: int, knots: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
    history: Set[Tuple[int, int]] = set()
    
    for move in range(magnitude):
        knots = step(direction, knots)
        history.add(knots[-1])

    return knots, history 

def simulate(vectors: List[Tuple[str, int]], length: int=2) -> int:
    knots = [(0, 0)] * length 
    positions: Set[Tuple[int, int]] = set()

    for direction, magnitude in vectors:
        knots, history = steps(direction, magnitude, knots)
        positions |= history

    return len(positions)
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vectors = load_vectors(sys.argv[1])
    else:
        vectors = load_vectors()

    print(f'For a rope of 2 knots, number of positions for the tail:  {simulate(vectors)}')
    print(f'For a rope of 10 knots, number of positions for the tail: {simulate(vectors, 10)}')

