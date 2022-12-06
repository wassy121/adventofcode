#!/usr/bin/env python3

import sys

from typing import *

from more_itertools import windowed # sliding window tool

def load_signal(input_file: str='input.txt') -> str:
    with open(input_file, 'r') as fp:
        return fp.readline().strip()

def get_start(signal: str, width: int) -> int:
    generator = (index for index, window in enumerate(windowed(signal, width), width) if len(set(window)) == width)
    return next(generator, 0) # return first occurence

def get_packet_start(signal: str) -> int:
    return get_start(signal, width=4)

def get_message_start(signal: str) -> int:
    return get_start(signal, width=14)

signal = load_signal()

get_packet_start(signal)
get_message_start(signal)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        signal = load_signal(sys.argv[1])
    else:
        signal = load_signal()

    print(f'Start of packet:  {get_packet_start(signal)}')
    print(f'Start of message: {get_message_start(signal)}')

