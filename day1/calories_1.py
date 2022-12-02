#!/usr/bin/env python3

import sys

from typing import *

import numpy as np
import pandas as pd

def top_elf_calories(input_file: str='input.txt') -> int:
    # load file, preserving blank separator rows
    with open('input.txt', 'r') as fp:
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

    # count the calories per elf
    sum_df = df.groupby('elf').sum('calories').reset_index()
    
    # return the most calories per elf
    return df.groupby('elf').sum('calories').max().values[0]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        total = top_elf_calories(sys.argv[1])
    else:
        total = top_elf_calories()

    print(total)

