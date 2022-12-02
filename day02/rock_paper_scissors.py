#!/usr/bin/env python3

import sys

from typing import *

import numpy as np
import pandas as pd

values = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3
}

outcome_score = [0, 3, 6] # loss, draw, win

def score_1(row: pd.Series) -> int:
    move_1 = values[row['opponent']]
    move_2 = values[row['second']]
    outcome = (move_2 - move_1 + 1) % 3 # 0 - loss, 1 - draw, 2 - win
    score = move_2 + outcome_score[outcome]

    return score

def score_2(row: pd.Series) -> int:
    move_1 = values[row['opponent']]
    outcome = values[row['second']] - 1 # 0 - loss, 1 - draw, 2 - win
    move_2 = (move_1 + outcome + 1) % 3 + 1
    score = move_2 + outcome_score[outcome]

    return score

def score(input_file: str='input.txt') -> Tuple[int, int]:
    df = pd.read_csv(input_file, sep='\s+', header=None, names=['opponent', 'second'])

    df['score_1'] = df.apply(score_1, axis=1)
    df['score_2'] = df.apply(score_2, axis=1)

    return tuple(df[['score_1', 'score_2']].sum())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        score_1, score_2 = score(sys.argv[1])
    else:
        score_1, score_2 = score()

    print(f'score 1 is {score_1}, and score 2 is {score_2}')

