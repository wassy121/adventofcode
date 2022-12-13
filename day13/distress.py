#!/usr/bin/env python3

import os
import sys

from typing import *

from functools import cmp_to_key
from more_itertools import windowed

from math import prod

import json

def load_packet_pairs(input_file: str='input.txt') -> List[Tuple[List[Any], List[Any]]]:
    with open(input_file, 'r') as fp:
        lines = [''] + [line.strip() for line in fp.readlines()] + ['']

    indices = [index for index, line in enumerate(lines) if not line]

    return [tuple(json.loads(line) for line in lines[slice(before+1, after)]) for before, after in windowed(indices, 2)]

def is_integer(element: Any) -> bool:
    return isinstance(element, int)

def is_list(element: Any) -> bool:
    return isinstance(element, list)

def in_order(left: List[Any], right: List[Any]) -> int: # -1 in order, 0 equal, 1 out of order
    left_length, right_length = len(left), len(right)

    for lefty, righty in zip(left, right):
        if is_integer(lefty) and is_integer(righty):
            if lefty < righty:
                return -1
            elif lefty > righty:
                return 1
        elif is_list(lefty) and is_list(righty):
            determined = in_order(lefty, righty)
            if determined:
                return determined
        else: # i.e. exactly one value is an integer
            if is_integer(lefty) and is_list(righty):
                determined = in_order([lefty], righty)
            elif is_list(lefty) and is_integer(righty):
                determined = in_order(lefty, [righty])
            else: # bad input
                raise ValueError(f'Bad input "{lefty}", "{righty}"!')
            if determined:
                return determined

    # if we get here, it's still undetermined
    if left_length < right_length:
        return -1
    elif left_length > right_length:
        return 1

    return 0

def sum_in_order_indices(packets: List[Tuple[List[Any], List[Any]]]) -> int:
    indices = [index for index, (left, right) in enumerate(packets, 1) if in_order(left, right) < 0]

    return sum(indices)

def sort_packets(packets: List[Any]) -> List[Any]:
    return sorted(packets, key=cmp_to_key(in_order))

def decoder_key(packet_pairs: List[Tuple[List[Any], List[Any]]], divider_packet_pair: Tuple[List[Any], List[Any]]=([[2]], [[6]])) -> int:
    packets = [packet for packet_pair in packet_pairs + [divider_packet_pair] for packet in packet_pair]
    indices = [index for index, packet in enumerate(sort_packets(packets), 1) if packet in divider_packet_pair]

    return prod(indices)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        packet_pairs = load_packet_pairs(sys.argv[1])
    else:
        packet_pairs = load_packet_pairs()

    print(f'Sum of indices of in-order packet pairs:  {sum_in_order_indices(packet_pairs)}')
    print(f'Decoder key of distress signal:           {decoder_key(packet_pairs)}')

