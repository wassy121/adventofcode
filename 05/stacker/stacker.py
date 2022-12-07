#!/usr/bin/env python3

import logging
import os
import pdb
import string
import typing

class Stacker:
    stacks = []

    def __init__(self, file_name: str = "resources/starting_stack_arranged.txt") -> None:
        i=0
        # blank starting stack so array has natural index of 1
        self.stacks.append([])
        with open(file_name, "r") as input_file:
            for line in input_file:
                self.stacks.append([])
                i+=1
                for j in line.strip():
                    self.stacks[i].append(j)


    def applyMoves(self, file_name: str = "resources/moves.txt") -> typing.List[str]:
        with open(file_name, "r") as input_file:
            for line in input_file:
                num_to_move = line.split()[1]
                from_stack = line.split()[3]
                to_stack = line.split()[5]
                temp_stack = []
                for i in range(1, int(num_to_move) + 1):
                    temp_stack.append(self.stacks[int(from_stack)].pop())
                #pdb.set_trace()
                self.stacks[int(to_stack)] += temp_stack


    def applyBetterMoves(self, file_name: str = "resources/moves.txt") -> typing.List[str]:
        with open(file_name, "r") as input_file:
            for line in input_file:
                num_to_move = line.split()[1]
                from_stack = line.split()[3]
                to_stack = line.split()[5]
                #pdb.set_trace()
                temp_stack = self.stacks[int(from_stack)][-int(num_to_move):]
                del(self.stacks[int(from_stack)][-int(num_to_move):])
                self.stacks[int(to_stack)] += temp_stack



def main() -> None:
    stacker = Stacker() #"resources/test/starting_stack_arranged.txt")
    #stacker.applyMoves() #"resources/test/moves.txt")
    stacker.applyBetterMoves() #"resources/test/moves.txt")
    print(stacker.stacks)

if __name__ == "__main__":
    main()
