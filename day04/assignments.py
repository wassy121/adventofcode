#!/usr/bin/env python3

import sys

from typing import *

def load_pairs(input_file: str='input.txt') -> List[str]:
    with open(input_file, 'r') as fp:
        return [line.strip() for line in fp.readlines()]

def containment(pair: str) -> bool:
    assignments = [int(assignment) for string in pair.split(',') for assignment in string.split('-')]
    contains = (assignments[0] <= assignments[2]) & (assignments[1] >= assignments[3])
    contained_by = (assignments[0] >= assignments[2]) & (assignments[1] <= assignments[3])
    return contains | contained_by

def count_containments(pairs: List[str]) -> int:
    containments = [containment(pair) for pair in pairs]
    return sum(containments) 

def overlap(pair: str) -> bool:
    assignments = [int(assignment) for string in pair.split(',') for assignment in string.split('-')]
    return (assignments[0] <= assignments[3]) & (assignments[1] >= assignments[2])
    
def count_overlaps(pairs: List[str]) -> int:
    overlaps = [overlap(pair) for pair in pairs]
    return sum(overlaps) 


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pairs = load_pairs(sys.argv[1])
    else:
        pairs = load_pairs()

    print(f'Number of assignment containments: {count_containments(pairs)}')
    print(f'Number of assignment overlaps: {count_overlaps(pairs)}')

