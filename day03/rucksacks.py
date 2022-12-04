#!/usr/bin/env python3

import sys

from string import ascii_lowercase as lowercase, ascii_uppercase as uppercase

from typing import *

priorities = {k: v for k, v in zip(lowercase + uppercase, range(1, 53))}

def find_error(rucksack: str) -> str:
    half = len(rucksack)//2
    compartments = [rucksack[:half], rucksack[half:]]
    return [item for item in set.intersection(*map(set, compartments))][0]

def find_errors(rucksacks: List[str]) -> List[str]:
    return [find_error(rucksack) for rucksack in rucksacks]

def sum_error_priorities(rucksacks: List[str]) -> int:
    priority_list = [priorities[error] for error in find_errors(rucksacks)]
    return sum(priority_list) 

def find_badge(group: Tuple[str]) -> str:
    return [item for item in set.intersection(*map(set, group))][0]

def find_badges(rucksacks: List[str]) -> List[int]:
    return [find_badge(group) for group in [*zip(*[iter(rucksacks)]*3)]]

def sum_badge_priorities(rucksacks: List[str]) -> int:
    priority_list = [priorities[badge] for badge in find_badges(rucksacks)]
    return sum(priority_list) 

def load_rucksacks(input_file: str='input.txt') -> List[str]:
    with open(input_file, 'r') as fp:
        return [line.strip() for line in fp.readlines()]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        rucksacks = load_rucksacks(sys.argv[1])
    else:
        rucksacks = load_rucksacks()

    print(f'Sum of error priorities: {sum_error_priorities(rucksacks)}')
    print(f'Sum of badge priorities: {sum_badge_priorities(rucksacks)}')

