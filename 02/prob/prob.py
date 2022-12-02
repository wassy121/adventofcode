#!/usr/bin/env python3

import logging
import pdb
import os
import typing

move_map = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

strategy_map = {
    "A": 1, # rock
    "B": 2, # paper
    "C": 3, # scissors
    "X": 0, # lose
    "Y": 3, # draw
    "Z": 6, # win
}



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

    def playGame(self, move1, move2):
        # self.player1_score += self.getRoundScore(move_map[move1], move_map[move2])
        # self.player2_score += self.getRoundScore(move_map[move2], move_map[move1])
        self.player2_score += self.getStrategyScore(move1, move2)

    def getStrategyScore(self, their_move: str, my_outcome: str) -> int:
        # pdb.set_trace()

        if their_move == "A":
            if my_outcome == "X": # lose
                return self.getRoundScore("Z", their_move)
            elif my_outcome == "Y": # draw
                return self.getRoundScore("X", their_move)
            elif my_outcome == "Z": # win
                return self.getRoundScore("Y", their_move)
        if their_move == "B":
            if my_outcome == "X": # lose
                return self.getRoundScore("X", their_move)
            elif my_outcome == "Y": # draw
                return self.getRoundScore("Y", their_move)
            elif my_outcome == "Z": # win
                return self.getRoundScore("Z", their_move)
        if their_move == "C":
            if my_outcome == "X": # lose
                return self.getRoundScore("Y", their_move)
            elif my_outcome == "Y": # draw
                return self.getRoundScore("Z", their_move)
            elif my_outcome == "Z": # win
                return self.getRoundScore("X", their_move)



    def getRoundScore(self, my_move, their_move) -> int:
        # pdb.set_trace()
        round_score = 0
        if move_map[my_move] == "rock":
            round_score += 1
        elif move_map[my_move] == "paper":
            round_score += 2
        elif move_map[my_move] == "scissors":
            round_score += 3

        # there is surely a sneakier way to do this
        if move_map[my_move] == move_map[their_move]:  # draw
            round_score += 3
        elif move_map[my_move] == "rock":
            if move_map[their_move] == "scissors":  # win
                round_score += 6
            elif move_map[their_move] == "paper":  # loss
                round_score += 0
        elif move_map[my_move] == "scissors":
            if move_map[their_move] == "rock":  # loss
                round_score += 0
            elif move_map[their_move] == "paper":  # win
                round_score += 6
        elif move_map[my_move] == "paper":
            if move_map[their_move] == "rock":  # win
                round_score += 6
            elif move_map[their_move] == "scissors":  # loss
                round_score += 0

        return round_score


# total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won)


def main() -> None:
    file_reader = FileReader("resources/input.txt")
    scores = file_reader.parse()
    print(str(scores))


if __name__ == "__main__":
    main()
