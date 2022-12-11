#!/usr/bin/env python3

import os
import sys

from typing import *
from numpy.typing import NDArray 

import re

import numpy as np

def load_program(input_file: str='input.txt') -> List[str]:
    with open(input_file, 'r') as fp:
        return [line.strip() for line in fp.readlines()]

addx_pattern = re.compile(r'addx (-?\d+)')

def execute(program: List[str], addx_pattern: re.Pattern=addx_pattern) -> NDArray[np.int_]:
    x = np.array([999, 1]) # cycle "0" (plus leading flag for indexing purposes)

    for instruction in program:
        x = np.append(x, x[-1])
        if instruction.startswith('addx'):
            increment = int(addx_pattern.match(instruction).group(1))
            x = np.append(x, x[-1] + increment)
        elif instruction == 'noop':
            pass # already handled by first append above
        else:
            raise ValueError('Illegal instruction!')

    return x

def sum_of_signal_strengths(program: List[str]) -> int:
    register = execute(program)
    indices = range(20, len(register) + 2, 40)

    return np.dot(indices, register[indices])

def render(program: List[str]):
    register = execute(program)

    for cycle, sprite in enumerate(register[1:-1], 1):
        position = (cycle - 1) % 40
        if abs(sprite - position) <= 1:
            print('#', end='')
        else:
            print('.', end='')
        if not cycle % 40:
            print()
            

if __name__ == "__main__":
    if len(sys.argv) > 1:
        program = load_program(sys.argv[1])
    else:
        program = load_program()

    print(f'The sum of the six signal strengths: {sum_of_signal_strengths(program)}')
    print(f'The eight capital letters from CRT:\n')
    render(program)

