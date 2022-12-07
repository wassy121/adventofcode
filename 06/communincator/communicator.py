#!/usr/bin/env python3

import logging
import os
import pdb
import string
import typing

class Communicator:
    comm_contents = ""


    def __init__(self, file_name: str = "resources/input.txt") -> None:
        with open(file_name, "r") as input_file:
            for line in input_file:
                self.comm_contents = line

    def getPacketMarker(self) -> int:
        for i in range(4, len(self.comm_contents)+1):
            if len({*self.comm_contents[i-4:i]}) == 4:
                return i

def main() -> None:
    communicator = Communicator() #"resources/test/input.txt")
    mark = communicator.getPacketMarker()
    print(mark)

if __name__ == "__main__":
    main()
