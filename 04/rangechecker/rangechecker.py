#!/usr/bin/env python3

import logging
import os
import pdb
import string
import typing

class RangeChecker:
    ranges = []


    def __init__(self, file_name: str = "input.txt") -> None:
        with open(file_name, "r") as input_file:
            for line in input_file:
                self.ranges.append(line.strip().split(','))

    def getPartialOverlaps(self):
        overlaps = []
        for range_set in self.ranges:
            # turn into string 23456 and 234 to see if one contains the other
            range_string0 = ''
            range_string1 = ''
            range_0 = [i for i in range(int(range_set[0].split('-')[0]), int(range_set[0].split('-')[1]) + 1)]
            for i in range(int(range_set[1].split('-')[0]), int(range_set[1].split('-')[1]) + 1):
                if i in range_0:
                    overlaps.append(str(range_set))
                    break
        return overlaps
#            pdb.set_trace()


    def getFullOverlaps(self):
        overlaps = []
        for range_set in self.ranges:
            # turn into string 23456 and 234 to see if one contains the other
            range_string0 = ''
            range_string1 = ''
            for i in range(int(range_set[0].split('-')[0]), int(range_set[0].split('-')[1]) + 1):
                range_string0 += f",{i},"
            for i in range(int(range_set[1].split('-')[0]), int(range_set[1].split('-')[1]) + 1):
                range_string1 += f",{i},"
#            pdb.set_trace()
            if range_string0.__contains__(range_string1) or range_string1.__contains__(range_string0):
                overlaps.append(str(range_set))
        return overlaps



def main() -> None:
    rangeChecker = RangeChecker("resources/input.txt")

    #overlaps = rangeChecker.getFullOverlaps()
    overlaps = rangeChecker.getPartialOverlaps()
    print(len(overlaps))


if __name__ == "__main__":
    main()
