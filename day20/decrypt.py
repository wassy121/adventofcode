#!/usr/bin/env python3

import os
import sys

from typing import *
from numpy.typing import NDArray

from operator import add
from functools import reduce

import numpy as np

def load_encryption(input_file: str='input.txt') -> NDArray[np.int64]:
    return np.loadtxt(input_file, dtype=np.int64)

def decrypt(encryption: NDArray[np.int64], with_key: bool=False, key: int=811589153) -> Tuple[NDArray[np.int64], NDArray[np.int64]]:
    modulus = len(encryption)
    encrypted = encryption.copy()

    new_indices = np.arange(modulus)

    if with_key:
        encrypted *= key
        times = 10
    else:
        times = 1

    for mix in range(times):
        for old_index, delta in enumerate(encrypted):
            new_index = np.flatnonzero(new_indices == old_index)[0] # no sorting
            new_indices = np.roll(new_indices, -new_index) # rotate element to move all the way to the left
            new_indices[1:] = np.roll(new_indices[1:], -delta) # rotate the rest in opposite direction to this element

    return encrypted[new_indices], new_indices

def coordinates(encryption: NDArray[np.int64], with_key: bool=False) -> Tuple[int, int, int]:
    modulus = len(encryption)

    decrypted, new_indices = decrypt(encryption, with_key=with_key)

    zero_index = np.flatnonzero(decrypted == 0)[0]

    rotated = np.roll(decrypted, -zero_index)

    return tuple(rotated[index % modulus] for index in [1000, 2000, 3000])

def sum_coordinates(encryption: NDArray[np.int64], with_key: bool=False) -> int:
    return reduce(add, coordinates(encryption, with_key=with_key))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        encryption = load_encryption(sys.argv[1])
    else:
        encryption = load_encryption()

    print(f'The sum of coordinates without key decryption:  {sum_coordinates(encryption, with_key=False)}')
    print(f'The sum of coordinates with key decryption:     {sum_coordinates(encryption, with_key=True)}')

