#!/usr/bin/env python3

import logging
import os
import pdb
import string
import typing


scores = [0] + list(string.ascii_letters)


class Rucksack:
    sack_contents = []

    def __init__(self, file_name: str = "input.txt") -> None:
        with open(file_name, "r") as input_file:
            for line in input_file:
                self.sack_contents.append(line.strip())

    def __findDuplicate(self, sack: str) -> str:
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
            duplicates.append(self.__findDuplicate(sack))
        return duplicates

    def getBadges(self) -> typing.List[str]:
        sack_group = []
        badges = []
        for index, sack in enumerate(self.sack_contents):
            sack_group.append(sack)
            if (index + 1) % 3 == 0 and index != 0:
                group_badges = list(
                    set(sack_group[0]) & set(sack_group[1]) & set(sack_group[2])
                )[0]
                assert len(group_badges) == 1
                badges += group_badges[0]
                sack_group = []
        return badges


def main() -> None:
    rucksack = Rucksack("resources/input.txt")

    duplicate_priorities = 0
    for dupe in Rucksack.getDuplicates(rucksack):
        duplicate_priorities += scores.index(dupe)
    print("duplicate score: {}".format(duplicate_priorities))

    badge_priorities = 0
    for badge in Rucksack.getBadges(rucksack):
        badge_priorities += scores.index(badge)
    print("badge score: {}".format(badge_priorities))


if __name__ == "__main__":
    main()
