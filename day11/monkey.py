#!/usr/bin/env python3

import os
import sys

from typing import *

from operator import add, mul, pow
from math import prod

from more_itertools import windowed

import re

class Monkey:
    __inspection_count: int

    __index: int
    __items: List[int]
    __operator: Callable[[int, int], int]
    __argument: int
    __modulus: int
    __true_index: int
    __false_index: int

    __primorial: int = prod([2, 3, 5, 7, 11, 13, 17, 19, 23])

    __patterns = [
        re.compile(r'^Monkey (\d+):$'),
        re.compile(r'\d+'),
        re.compile(r'^Operation: new = old ([\+\*]) ([\d|\w]+)$'),
        re.compile(r'^Test: divisible by (\d+)$'),
        re.compile(r'^If true: throw to monkey (\d+)$'),
        re.compile(r'^If false: throw to monkey (\d+)$')
    ]

    def __init__(self, lines: List[str]) -> None:
        self.__inspection_count = 0
        for index, line in enumerate(lines):
            if index == 1:
                arguments = [*map(int, self.__patterns[index].findall(line))]
                self.__items = arguments
            elif index == 2:
                arguments = self.__patterns[index].match(line).groups()
                if arguments[-1] == 'old':
                    self.__operator = pow
                    self.__argument = 2
                else:
                    self.__argument = int(arguments[-1])
                    if arguments[0] == '+':
                        self.__operator = add
                    else: # == '*'
                        self.__operator = mul
            else:
                argument = int(self.__patterns[index].match(line).group(1))
                if index == 0:
                    self.__index = argument
                elif index == 3:
                    self.__modulus = argument
                elif index == 4:
                    self.__true_index = argument
                elif index == 5:
                    self.__false_index = argument

    def __str__(self) -> str:
        return f'Monkey {self.__index}:\n' + \
            f'  Items: {", ".join([str(item) for item in self.__items])}\n' + \
            f'  Operation: new = old {self.__operator.__name__} {self.__argument}\n' + \
            f'  Test: divisible by {self.__modulus}\n' + \
            f'    If true: throw to monkey {self.__true_index}\n' + \
            f'    If false: throw to monkey {self.__false_index}\n'

    def __operation(self, old: int, argument: int) -> int:
        return self.__operator(old, argument)

    def get_inspection_count(self) -> int:
        return self.__inspection_count

    def add_item(self, item: int) -> None:
        self.__items.append(item)

    def inspect(self, relief: bool=True) -> List[Tuple[int, int]]:
        fate: List[Tuple[int, int]] = []

        for item in self.__items:
            self.__inspection_count += 1

            # inspection begins
            worry_level = self.__operation(item, self.__argument)
            
            if relief:
                # monkey get bored with item
                worry_level //= 3
            else:
                # "... find another way to keep your worry levels manageable."
                # i.e. prevent overflow without changing divisibility FOR ANY MONKEY
                # e.g. c.f. Chinese Reminder Theorem
                worry_level %= self.__primorial # product of all (prime) required modulii
            
            # test
            if not worry_level % self.__modulus: # i.e. if divisible
                result = (self.__true_index, worry_level)
            else:
                result = (self.__false_index, worry_level)
            fate.append(result)    

        self.__items = [] # clear

        return fate # who and what to throw


def load_monkeys(input_file: str='input.txt') -> List[Monkey]:
    with open(input_file, 'r') as fp:
        lines = [''] + [line.strip() for line in fp.readlines()] + ['']

    indices = [index for index, line in enumerate(lines) if not line]
    monkeys: List[Monkey] = [Monkey(lines[slice(before+1, after)]) for before, after in windowed(indices, 2)] 

    return monkeys

def round(monkeys: List[Monkey], relief: bool=True) -> List[Monkey]:
    for i in range(len(monkeys)):
        # transfer items between monkeys
        for j, item in monkeys[i].inspect(relief):
            monkeys[j].add_item(item) 

    return monkeys

def rounds(monkeys: List[Monkey], number_rounds: int, relief: bool=True) -> List[Monkey]:
    for i in range(number_rounds):
        monkeys = round(monkeys, relief=relief)
    
    return monkeys

def monkey_business(monkeys: List[Monkey]) -> int:
    two_most_active = sorted([monkey.get_inspection_count() for monkey in monkeys], reverse=True)[:2]
    return mul(*two_most_active)

def shenanigans(monkeys: List[Monkey], number_rounds: int, relief: bool=True) -> int:
    monkeys = rounds(monkeys, number_rounds=number_rounds, relief=relief)

    return monkey_business(monkeys)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        monkeys_20 = load_monkeys(sys.argv[1])
        monkeys_10000 = load_monkeys(sys.argv[1])
    else:
        monkeys_20 = load_monkeys()
        monkeys_10000 = load_monkeys()

    print(f'Monkey business for 20 rounds of shenanigans with relief:        {shenanigans(monkeys_20, 20)}')
    print(f'Monkey business for 10,000 rounds of shenanigans without relief: {shenanigans(monkeys_10000, 10_000, relief=False)}')

