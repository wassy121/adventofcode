#!/usr/bin/env python3

import logging
import os
import typing


class FileReader:
    file_name = "input.txt"

    def __init__(self, file_name: str = "input.txt") -> None:
        self.file_name = file_name
        pass

    def parse(self) -> typing.List[int]:
        return_list = []
        with open(self.file_name, "r") as input_file:
            backpack = Backpack()
            for line in input_file:
                if line == "\n":
                    return_list.append(backpack.getCalories())
                    backpack = Backpack()
                else:
                    backpack.addCalories(int(line))
            # be sure to add the final backpack contents to the return list
            return_list.append(backpack.getCalories())
        return return_list


class Backpack:
    calorie_content = 0

    def __init__(self, initial_calories: int = 0) -> None:
        self.calorie_content = initial_calories

    def addCalories(self, num_calories: int) -> None:
        self.calorie_content += num_calories

    def getCalories(self) -> int:
        return self.calorie_content


def main() -> None:
    file_reader = FileReader('resources/input.txt')
    elf_list = file_reader.parse()
    print(max(elf_list))


if __name__ == "__main__":
    main()
