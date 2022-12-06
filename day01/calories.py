#!/usr/bin/env python3

import sys

from typing import *

import numpy as np
import pandas as pd

def parse_input(input_file: str) -> pd.DataFrame:
    # load file, preserving blank separator rows
    with open(input_file, 'r') as fp:
        lines = [line.strip() for line in fp.readlines()]
    
    # add trailing blank separator to allow for backfilling later
    lines.append('')

    # convert calories to dataframe, replacing blanks with -1, and then add elf column placeholder
    df = pd.DataFrame(lines, columns=['calories']).replace('', -1).astype(np.int64)
    df['elf'] = np.nan
    
    # enumerate negative calories (i.e. prior blanks) into the elf column
    i = 1
    for index in df[df['calories'] < 0].index:
      df['elf'].at[index] = i
      i += 1

    # backfill the elf column to identify the group of calories for the elf
    df['elf'] = df['elf'].fillna(method='bfill').astype(np.int64)
    df = df[df['calories'] >= 0]

    return df

def top_elf_calories(input_file: str='input.txt') -> int:
    df = parse_input(input_file)

    # return the most total calories per elf
    return df.groupby('elf').sum('calories').max().values[0]

def top_k_elves_calories(input_file: str='input.txt', k: int=3) -> int:
    df = parse_input(input_file)

    # return the total calories per the top k elves
    return df.groupby('elf').sum('calories').sort_values('calories', ascending=False)['calories'].values[:k].sum()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        top_calories = top_elf_calories(sys.argv[1])
        top_k_calories = top_k_elves_calories(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) > 1:
        top_calories = top_elf_calories(sys.argv[1])
        top_k_calories = top_k_elves_calories(sys.argv[1])
    else:
        top_calories = top_elf_calories()
        top_k_calories = top_k_elves_calories()

    print(f'Total calories for top elf:     {top_calories}')
    print(f'Total calories for top k elves: {top_k_calories}')
