#!/usr/bin/env python3

import os
import sys

from typing import *

from operator import sub, ge, le

import re

arrangement_pattern = re.compile(r'^Sensor at x=([-+]?\d+), y=([-+]?\d+): closest beacon is at x=([-+]?\d+), y=([-+]?\d+)')

def load_arrangement(input_file: str='input.txt', arrangement_pattern: re.Pattern=arrangement_pattern) -> List[List[Tuple[int, int]]]:
    with open(input_file, 'r') as fp:
        lines = [line.strip() for line in fp.readlines()]

    tuples = [tuple(int(element) for element in arrangement) for line in lines for arrangement in arrangement_pattern.findall(line)]

    return [[(sx, sy), (bx, bc)] for (sx, sy, bx, bc) in tuples]
    
def distance(point1: Tuple[int, int], point2: Tuple[int, int]):
    # Manhattan distance
    return sum(map(lambda a, b: abs(sub(a, b)), point1, point2))
    
def cut_diamond(center: Tuple[int, int], radius: int, y0: int) -> List[Tuple[int, int]]:
    # based on L1-Norm "circle" using the Manhattan metric
    xc, yc = center

    dy = abs(y0 - yc)
    if dy > radius:
        return [] # empty
    
    return [(x0, y0) for x0 in range(xc + dy - radius, xc + radius - dy + 1)]

def report(arrangements: List[List[Tuple[int, int]]], y0: int) -> Set[Tuple[int, int]]:
    vacancy: List[Tuple[int, int]] = []

    hardware: Set[Tuple[int, int]] = {hardware for arrangement in arrangements for hardware in arrangement if hardware[1] == y0} # beacon not colocated at sensor

    for sensor, beacon in arrangements:
        r = distance(sensor, beacon)
        vacancy.extend(cut_diamond(sensor, r, y0))
    
    return set(vacancy) - hardware

def count(arrangements: List[List[Tuple[int, int]]], y0: int) -> int:
    vacant = report(arrangements, y0)

    return len(vacant)

def scan(arrangements: List[List[Tuple[int, int]]], maximum: int, minimum: int=0) -> Tuple[int, int]:
    def bounded_x_interval(center: Tuple[int, int], radius: int, y0: int) -> List[int]:
        # based on L1-Norm "circle" using the Manhattan metric
        xc, yc = center

        dy = abs(y0 - yc)
        if dy > radius:
            return [] # empty

        return [max(minimum, xc + dy - radius), min(maximum, xc + radius - dy + 1)]

    # See:  https://www.geeksforgeeks.org/merging-intervals/
    def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
    
        index = 0
        for i in range(1, len(intervals)):
            if (intervals[index][1] >= intervals[i][0]):
                intervals[index][1] = max(intervals[index][1], intervals[i][1])
            else:
                index += 1
                intervals[index] = intervals[i]
        return [intervals[i] for i in range(index+1)]

    for y0 in range(maximum, minimum - 1, -1):
        x_intervals: List[List[int]] = []
        for sensor, beacon in arrangements:
            r = distance(sensor, beacon)
            x_range = bounded_x_interval(sensor, r, y0)
            if x_range:
                x_intervals.append(x_range)
        x_intervals = merge_intervals(x_intervals)
        
        if len(x_intervals) > 1:
            # distress beacon found in between the intervals
            x0 = x_intervals[0][-1]
            return x0, y0

    return -1, -1
    
def tuning_frequency(arrangements: List[List[Tuple[int, int]]], maximum: int, minimum: int=0) -> int:
    x0, y0 = scan(arrangements, minimum=minimum, maximum=maximum)

    return 4_000_000 * x0 + y0
    

if __name__ == "__main__":
    y = 2_000_000
    maximum = 4_000_000
    if len(sys.argv) > 1:
        arrangements = load_arrangement(sys.argv[1])
    else:
        arrangements = load_arrangement()
    if len(sys.argv) > 2:
        y = int(sys.argv[2])
    if len(sys.argv) > 3:
        maximum = int(sys.argv[3])

    print(f'At y={y}, count of positions that cannot contain a beacon:  {count(arrangements, y0=y)}')
    print(f'The tuning frequency between 0 and {maximum}:                     {tuning_frequency(arrangements, maximum=maximum)}')

