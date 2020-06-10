import copy
import random
import sys

import numpy as np

from board import Board
from position import Position


class GameMove(object):
    def __init__(self, value, pos_from: Position, pos_to: Position):
        self.pos_from = pos_from
        self.pos_to = pos_to
        self.value = value

    def __repr__(self):
        return "from:" + str(self.pos_from) + " to:" + str(self.pos_to) + " v:" + str(self.value)


class GameState(object):
    P1 = 1
    P2 = -1

    def __init__(self, state, next_to_move=1, c_move=None):
        self.board = state
        self.board_size = 9
        self.next_to_move = next_to_move
        self.current_move = c_move

    @property
    def game_result(self):
        # check if game is over
        status = self.board.checkStatus()
        if status == 1:
            return 1.
        elif status == -1:
            return -1.
        else:
            # if not over - no result
            return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        return self.board.move_check(move.value, move.pos_to.y, move.pos_to.x)


    def move(self, move):
        new_board = copy.deepcopy(self.board)
        new_board.performMove(move.value, move.pos_from, move.pos_to)
        next_to_move = GameState.P2 if self.next_to_move == GameState.P1 else GameState.P1
        return GameState(new_board, next_to_move, move)

    def get_legal_actions(self):
        possibleStates = []
        player = self.next_to_move
        availableMoves = self.board.getPossibleMoves(player)
        for move in availableMoves:
            pos_from = Position(y=move[player]['from'][0], x=move[player]['from'][1])
            pos_to = Position(y=move[player]['to'][0], x=move[player]['to'][1])
            possibleStates.append(GameMove(self.next_to_move, pos_from, pos_to))
        return possibleStates
