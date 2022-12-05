#!/usr/bin/env python3

import sys

from typing import *
from typing import *

import re

import numpy as np

move_pattern = re.compile(r'^move (\d+) from (\d+) to (\d+)\s*$')

def get_stacks(levels: List[str]) -> List[List[str]]:
    grid = [[quadruple[1] for quadruple in [*zip(*[iter(level)]*4)]] for level in levels]
    grid = np.array(grid)
    
    stacks = [['']]
    for column in range(grid.shape[1]):
        stacks.append([cell for cell in grid[-2::-1, column].tolist() if cell.strip()])

    return stacks

def get_moves(procedures: List[str]) -> List[Tuple[int, int, int]]:
    return [(*map(int, move_pattern.findall(procedure)[0]),) for procedure in procedures]

def parse_input(input_file: str) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
    with open(input_file, 'r') as fp:
        lines = fp.readlines() # no stripping due to parsing below
    
    blank_index = [index for index, line in enumerate(lines) if not line.strip()][0]
    
    levels = lines[:blank_index]
    stacks = get_stacks(levels)

    procedures = lines[blank_index+1:]
    moves = get_moves(procedures)

    return stacks, moves

def execute_3000(input_file: str='input.txt') -> str:
    stacks, moves = parse_input(input_file)
    
    for quantity, source, destination in moves:
        for each in range(quantity):
            crate = stacks[source].pop()
            stacks[destination].append(crate)

    return ''.join([stack[-1] for stack in stacks])

def execute_3001(input_file: str='input.txt') -> str:
    stacks, moves = parse_input(input_file)
    
    for quantity, source, destination in moves:
        crates = stacks[source][-quantity:]
        del stacks[source][-quantity:]
        stacks[destination].extend(crates)

    return ''.join([stack[-1] for stack in stacks])
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tops1 = execute_3000(sys.argv[1])
        tops2 = execute_3001(sys.argv[1])
    else:
        tops1 = execute_3000()
        tops2 = execute_3001()

    print(f'Crates at top for CrateMaster 3000 after procedure: "{tops1}"')
    print(f'Crates at top for CrateMaster 3001 after procedure: "{tops2}"')

