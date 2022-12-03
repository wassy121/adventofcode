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
        first_half = sack[slice(0, len(sack) // 2)]
        second_half = sack[
            len(sack) // 2 if len(sack) % 2 == 0 else ((len(sack) // 2) + 1) :
        ]
        duplicates = list(set(first_half) & set(second_half))
        assert len(duplicates) == 1
        return duplicates[0]

    def getDuplicates(self) -> typing.List[str]:
        duplicates = []
        for sack in self.sack_contents:
            duplicates.append(self.findDuplicate(sack))
        return duplicates

    def getBadges(self) -> typing.List[str]:
        sack_group = []
        badges = []
        for index, sack in enumerate(self.sack_contents):
            sack_group.append(sack)
            if (index + 1) % 3 == 0 and index != 0:
                badges += list(
                    set(sack_group[0]) & set(sack_group[1]) & set(sack_group[2])
                )[0]
                sack_group = []

        return badges


def main() -> None:
    rucksack = Rucksack("resources/input.txt")

    final_score = 0
    badge_score = 0
    duplicates = Rucksack.getDuplicates(rucksack)
    for dupe in duplicates:
        final_score += scores.index(dupe) + 1  # 0-indexed arrays
    print("duplicate score: {}".format(final_score))
    badges = Rucksack.getBadges(rucksack)
    for badge in badges:
        badge_score += scores.index(badge) + 1  # 0-indexed arrays
    print("badge score: {}".format(badge_score))


if __name__ == "__main__":
    main()
