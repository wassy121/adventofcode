#!/usr/bin/env python3

import os
import sys

from typing import *
from numpy.typing import NDArray

from operator import eq, add, sub, mul, floordiv
from math import gcd

from functools import reduce

import numpy as np
from numpy.polynomial.polynomial import Polynomial

import re

class Monkey:
    __name: str

    __number: int
    __left_name: str
    __right_name: str
    __operator: Union[Callable[[Union[int, Polynomial], Union[int, Polynomial]], Union[int, Polynomial]], None]

    __directory: Dict[str, 'Monkey']

    __patterns = [
        re.compile(r'^(\w+): (\d+)$'),
        re.compile(r'^(\w+): (\w+) ([\+\-\*\/]) (\w+)$')
    ]

    def __init__(self, line: str) -> None:
        arguments = []
        for equation, pattern in enumerate(self.__patterns):
            matched = pattern.match(line)
            if matched:
                arguments = matched.groups()
                break

        self.__name = arguments[0]
        if not equation:
            self.__number = int(arguments[1])
            self.__operator = None
        else: # if is equation
            self.__left_name, self.__right_name = arguments[1], arguments[3]
            if arguments[2] == '+':
                self.__operator = add
            elif arguments[2] == '-':
                self.__operator = sub
            elif arguments[2] == '*':
                self.__operator = mul
            else:
                self.__operator = floordiv

    def __str__(self) -> str:
        if self.__operator is None:
            return f'{self.__name}: {self.__number}'
        return f'{self.__name}: {self.__left_name} {self.__operator.__name__} {self.__right_name}'

    def get_name(self) -> str:
        return self.__name

    def set_directory(self, directory: Dict[str, 'Monkey']) -> None:
        self.__directory = directory

    def yell(self) -> int:
        if self.__operator is None:
            return self.__number
        return self.__operator(self.__directory[self.__left_name].yell(), self.__directory[self.__right_name].yell())

    def __reduce(self, numerator: Polynomial, denominator: Polynomial) -> Tuple[Polynomial, Polynomial]:
        divisor = reduce(gcd, map(int, np.append(numerator.coef, denominator.coef)))
        return numerator / divisor, denominator / divisor

    # to solve for human
    def solve(self) -> Union[Tuple[Polynomial, Polynomial], int]: # polynomial numerator, polynomial denominator OR root of polynomial
        if self.__operator is None:
            if self.__name == 'humn':
                return Polynomial([0, 1]), Polynomial([1]) # i.e. "x" = (0 + 1 x) / 1
            else:
                return Polynomial([self.__number]), Polynomial([1]) # i.e. "n" = n / 1

        numerator1, denominator1 = self.__directory[self.__left_name].solve()
        numerator2, denominator2 = self.__directory[self.__right_name].solve()
        if self.__name == 'root':
            # cross multiply and combine terms
            function = numerator1 * denominator2 - numerator2 * denominator1
            return int(function.roots()[0])

        operation = self.__operator.__name__
        if operation in ['add', 'sub']:
            numerator = self.__operator(numerator1 * denominator2, numerator2 * denominator1)
            denominator = denominator1 * denominator2
        elif operation == 'mul':
            numerator = self.__operator(numerator1, numerator2)
            denominator = self.__operator(denominator1, denominator2)
        else: # i.e. div
            numerator = numerator1 * denominator2
            denominator = numerator2 * denominator1
        return self.__reduce(numerator, denominator)

def load_monkeys(input_file: str='input.txt') -> Dict[str, Monkey]:
    with open(input_file, 'r') as fp:
        lines = [line.strip() for line in fp.readlines()]

        monkeys = [Monkey(line) for line in lines]

        directory = {monkey.get_name(): monkey for monkey in monkeys}

        for monkey in monkeys:
            monkey.set_directory(directory) # imbue with knowledge of other monkeys

        return directory


if __name__ == "__main__":
    if len(sys.argv) > 1:
        monkeys = load_monkeys(sys.argv[1])
    else:
        monkeys = load_monkeys()

    print(f"""The monkey named "root" yelled out:          {monkeys['root'].yell()}""")
    print(f"""To pass root's equality test, you yell out:  {monkeys['root'].solve()}""")

