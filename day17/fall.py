#!/usr/bin/env python3

import os
import sys

from typing import *

from functools import reduce

from operator import sub, mul, lshift, rshift
from math import gcd
lcm = lambda a, b: mul(a, b) // gcd(a, b) # not available until Python 3.9.0

from collections import deque

def binary(bits: Iterable[bool]) -> int:
    # Horner's method for binary
    return reduce(lambda a, b: a << 1 | b, bits)

def bits(binary: int, length: int=9) -> List[bool]:
    bits = [False] * length 
    index = length - 1 
    while binary:
         bits[index] = bool(binary & 1)
         binary >>= 1
         index -= 1
    
    return bits

def bit_count(binary: int) -> int:
    count = 0
    while binary:
        binary &= binary - 1
        count += 1
    return count

def load_jet(input_file: str='input.txt') -> Deque[Callable]:
    with open(input_file, 'r') as fp:
        return deque(map(lambda character: {'>': rshift, '<': lshift}[character], fp.readline().strip()))

def show_chamber(chamber: List[int]) -> None:
    rock_dict = {False: '.', True: '#'}
    wall_dict = {False: '.', True: '|'}
    floor_dict = {False: '.', True: '-'}
    corner_dict = {False: '.', True: '+'}
    for binary in chamber[:-1]:
        stratum = bits(binary)
        print(wall_dict[stratum[0]], end="")
        for pebble in stratum[1:-1]:
            print(rock_dict[pebble], end="")
        print(wall_dict[stratum[-1]], end="")
        print()
    floor = bits(chamber[-1])
    print(corner_dict[floor[0]], end="")
    for pebble in floor[1:-1]:
        print(floor_dict[pebble], end="")
    print(corner_dict[floor[-1]], end="")
    print()

def show_rock(rock: List[int]) -> None:
    rock_dict = {False: '.', True: '#'}
    for binary in rock:
        stratum = bits(binary)
        for pebble in stratum:
            print(rock_dict[pebble], end="")
        print()
    print()

def fall(chamber: List[int], rock: List[int], jet: Deque[Callable]) -> List[int]:
    def collision(strata1: List[int], strata2: List[int]) -> bool:
        return any(bit_count(stratum1 | stratum2) < bit_count(stratum1) + bit_count(stratum2) for stratum1, stratum2 in zip(strata1, strata2))

    def push(index: int, mask: List[int], shift: Callable) -> List[int]:
        cavern = chamber[index:index+len(mask)]

        new_mask = [*map(lambda stratum: shift(stratum, 1), mask)]

        stopped = collision(cavern, new_mask)
        if not stopped:
           return new_mask

        return mask

    def drop(index: int, mask: List[int]) -> Tuple[int, bool]:
        cavern = chamber[index+1:index+len(mask)+1]

        stopped = collision(cavern, mask)
        if not stopped:
            index += 1

        return index, stopped 

    # expand chamber
    walls = [binary([True] + [False]*7 + [True])] * (len(rock) + 3)
    chamber = walls + chamber

    # initialize index to introduce "mask"
    index = 0
    mask = rock.copy() # don't modify original rock

    # commence falling
    stopped = False
    while not stopped:
        # push rock
        mask = push(index, mask, jet[0])
        jet.rotate(-1)

        # drop rock
        index, stopped = drop(index, mask) # increments index if necessary

    # "burn" mask into chamber
    for j, stratum in enumerate(mask):
        chamber[index+j] |= stratum

    # "trim" chamber
    index = next(index for index, stratum in enumerate(chamber) if bit_count(stratum) > 2)
    return chamber[index:] 

# See:
# * [Finding period of a sequence](https://stackoverflow.com/questions/43678496/finding-period-of-a-sequence#43679787)
# * [Z algorithm (Linear time pattern searching Algorithm)](https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/)
# * [Z Algorithm](https://codeforces.com/blog/entry/3107)

def z_algorithm(s: List[int]) -> List[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i > r:
            l = r = i
            while r < n and s[r-l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < n and s[r-l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z

def period(pattern: List[int], sequence: List[int]) -> int:
    length = len(pattern)
    concat = pattern + [-1] + sequence

    z = z_algorithm(concat)

    matches = [i - length - 1 for i in range(len(concat)) if z[i] == length]

    if len(matches) > 1:
        return matches[1] - matches[0]

    return 0

def tee(heights: List[int], multiple: int) -> int:
    sequence = [*map(sub, heights[1:], heights[:-1])]
    m = len(heights) % multiple # get last "multiple" of heights

    if m < 1: # i.e. nothing to pattern match
        return 0
        
    pattern = sequence[slice((m-1)*multiple-1, m*multiple-1)]

    return period(pattern, sequence)

def stack(input_file: str='input.txt', iterations: int=2022) -> Tuple[List[int], int]:
    # initialize rocks
    rocks = deque([
        [
            binary([False, False, False,  True,  True,  True,  True, False, False])
        ],
        [
            binary([False, False, False, False,  True, False, False, False, False]),
            binary([False, False, False,  True,  True,  True, False, False, False]),
            binary([False, False, False, False,  True, False, False, False, False])
        ],
        [
            binary([False, False, False, False, False,  True, False, False, False]),
            binary([False, False, False, False, False,  True, False, False, False]),
            binary([False, False, False,  True,  True,  True, False, False, False])
        ],
        [
            binary([False, False, False,  True, False, False, False, False, False]),
            binary([False, False, False,  True, False, False, False, False, False]),
            binary([False, False, False,  True, False, False, False, False, False]),
            binary([False, False, False,  True, False, False, False, False, False])
        ],
        [
            binary([False, False, False,  True,  True, False, False, False, False]),
            binary([False, False, False,  True,  True, False, False, False, False])
        ]
       ]) 

    # initialize jet
    jet = load_jet(input_file) 

    # initialize chamber floor
    chamber = [binary([True] * 9)]

    multiple = lcm(len(jet), 5)
    if iterations < multiple:
        loops = iterations
    else:
        loops = multiple*100

    # begin stacking
    heights, t = [0], 0
    for iteration in range(loops):
        if not iteration:
            pass
        elif not iteration % 100_000:
            print(iteration, flush=True)
        elif not iteration % 10_000:
            print(iteration, end='', flush=True)
        elif not iteration % 1_000:
            print('.', end='', flush=True)
        chamber = fall(chamber, rocks[0], jet)
        heights.append(len(chamber) - 1)
        rocks.rotate(-1)
        if iteration > multiple and not iteration % multiple:
            t = tee(heights, multiple)
            if t:
                break

    if iteration >= 1_000:
        print()

    if not t:
        return chamber, heights[iterations]
        
    height = (heights[2*t] - heights[t]) * (iterations // t) + heights[iterations % t]

    return chamber, height


if __name__ == "__main__":
    iterations1 = 2022
    iterations2 = 1_000_000_000_000
    if len(sys.argv) > 1:
        _, height1 = stack(sys.argv[1], iterations=iterations1)
        _, height2 = stack(sys.argv[1], iterations=iterations2)
    else:
        _, height1 = stack(iterations=iterations1)
        _, height2 = stack(iterations=iterations2)

    print(f'The height after dropping {iterations1} rocks is: {height1}')
    print(f'The height after dropping {iterations2} rocks is: {height2}')

