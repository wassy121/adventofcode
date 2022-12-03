#!/usr/bin/env python3

import logging
import os
import pdb
import string
import typing


scores = list(string.ascii_letters)


class Rucksack:
    sack_contents = []

    def __init__(self, file_name: str = "input.txt") -> None:
        with open(file_name, "r") as input_file:
            for line in input_file:
                self.sack_contents.append(line.strip())

    def findDuplicate(self, sack: str) -> str:
        first_half  = sack[slice(0             , len(sack) // 2)]
        second_half = sack[len(sack)//2 if len(sack)%2 == 0
                                                 else ((len(sack)//2)+1):]
        #pdb.set_trace()
        return list(set(first_half) & set(second_half))[0]  # there should be only 1

    def getDuplicates(self):
        duplicates = []
        for sack in self.sack_contents:
            duplicates.append(self.findDuplicate(sack))
        return duplicates


def main() -> None:
    rucksack = Rucksack("resources/input.txt")

    final_score = 0
    duplicates = Rucksack.getDuplicates(rucksack)
    # duplicates.sort()
    for dupe in duplicates:
        final_score += scores.index(dupe) + 1 # 0-indexed arrays
    print (final_score)


if __name__ == "__main__":
    main()
