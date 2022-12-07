#!/usr/bin/env python3

import os
import sys

from typing import *

from collections import defaultdict

def traverse(input_file: str='input.txt') -> DefaultDict[str, int]:
    with open(input_file, 'r') as fp:
        tokens_list = [line.strip().split() for line in fp.readlines()]

    pwd = []
    files: DefaultDict[str, int] = defaultdict(lambda : 0, {os.path.sep: 0})

    for tokens in tokens_list:
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                if tokens[2] == '/':
                    pwd = [tokens[2]]
                elif tokens[2] == '..':
                    pwd.pop()
                else:
                    pwd.append(tokens[2])
            elif tokens[1] == 'ls':
                pass
            else:
                raise ValueError('unknown command!')
        elif tokens[0] == 'dir':
            files[f'{os.path.join(*pwd, tokens[1])}'] = 0
        else:
            files[f'{os.path.join(*pwd, tokens[1])}'] = int(tokens[0])

    return files

def du_s(files: DefaultDict[str, int]) -> DefaultDict[str, int]:
    directories = [directory for directory, size in files.items() if size == 0]

    dictionary = {directory: sum([size for file, size in files.items() if file.startswith(directory)]) for directory in directories}

    return defaultdict(lambda : 0, dictionary)

def total_smallest(files: DefaultDict[str, int], threshold: int=100_000) -> int:
    directories = du_s(files)

    return sum([size for directory, size in directories.items() if size <= threshold])

def total_deleted(files: DefaultDict[str, int], required: int=30_000_000, capacity: int=70_000_000) -> int:
    directories = du_s(files)
    used: int = directories[os.path.sep]
    available: int = capacity - used
    needed: int = required - available

    generator = (size for directory, size in sorted(directories.items(), key=lambda item: item[1]) if size >= needed)
    return next(generator, used) # first "big" enough to delete


if __name__ == "__main__":
    if len(sys.argv) > 1:
        files = traverse(sys.argv[1])
    else:
        files = traverse()

    print(f'Total of "smallest" directory trees:  {total_smallest(files)}')
    print(f'Total of "deleted" directory trees:   {total_deleted(files)}')

