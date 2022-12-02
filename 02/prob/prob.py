#!/usr/bin/env python3

import logging
import pdb
import os
import typing

move_map = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}
updated_move_map = {
    "A": "R",
    "B": "P",
    "C": "S",
}
strategy_map = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}
losers = ["RS", "PR", "SP"]
winners = ["RP", "PS", "SR"]


class FileReader:
    file_name = "input.txt"

    def __init__(self, file_name: str = "input.txt") -> None:
        self.file_name = file_name
        pass

    def parse(self) -> typing.List[int]:
        return_list = []
        with open(self.file_name, "r") as input_file:
            rps_fight = RPSFight()
            for line in input_file:
                moves = line.strip().split(" ")
                rps_fight.playGame(moves[0], moves[1])
        return_list = [rps_fight.player1_score, rps_fight.player2_score]
        return return_list


class RPSFight:
    player1_score = 0
    player2_score = 0

    def playGame(self, move1: str, move2: str) -> None:
        # first problem had different criteria
        # self.player1_score += self.getRoundScore(move_map[move1], move_map[move2])
        # self.player2_score += self.getRoundScore(move_map[move2], move_map[move1])
        self.player2_score += self.getStrategyScore(
            updated_move_map[move1], strategy_map[move2]
        )

    def getStrategyScore(self, their_move: str, my_outcome: str) -> int:

        # pdb.set_trace()
        if my_outcome == "lose":
            search_array = losers
        elif my_outcome == "win":
            search_array = winners
        if my_outcome == "draw":
            return self.getRoundScore(their_move, their_move)
        else:
            # moves = [i for i in search_array if i[0] == their_move][0]
            # return self.getRoundScore(moves[1:], their_move)
            #
            # not sure whether I like above or below better. Overly-clever code reduces maintainability
            for moves in search_array:
                if moves[0] == their_move:
                    return self.getRoundScore(moves[1:], their_move)

    def getRoundScore(self, my_move: str, their_move: str) -> int:
        round_score = 0
        if my_move == "R":
            round_score += 1
        elif my_move == "P":
            round_score += 2
        elif my_move == "S":
            round_score += 3

        if my_move == their_move:  # draw
            round_score += 3
        elif their_move + my_move in losers:
            round_score += 0
        else:  # win
            round_score += 6

        return round_score


# total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won)


def main() -> None:
    file_reader = FileReader("resources/input.txt")
    scores = file_reader.parse()
    print(str(scores))


if __name__ == "__main__":
    main()
