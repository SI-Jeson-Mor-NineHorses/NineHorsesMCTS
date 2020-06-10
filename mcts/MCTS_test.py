from board import Board
from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from state import GameState
from state import GameMove
from position import Position


def init():
    initial_board_state = GameState(state=Board(), next_to_move=1)
    root = MonteCarloTreeSearchNode(state=initial_board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(100)
    c_state = best_node.state
    c_board = c_state.board
    return c_state, c_board


def get_action(state):
    try:
        location = input("Your move: ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]
        if len(location) != 4:
            return -1
        x_from = location[0]
        y_from = location[1]

        x_to = location[2]
        y_to = location[3]
        pos_from = Position(x_from, y_from)
        pos_to = Position(x_to, y_to)

        move = GameMove(-1, pos_from, pos_to)
    except Exception as e:
        move = -1
    if move == -1 or not state.is_move_legal(move):
        print("invalid move")
        move = get_action(state)
    return move



c_state, c_board = init()
c_board.printBoard()
# graphics(c_board)
next_move = -1
while True:
    # move1 = get_action(c_state)
    # c_state = c_state.move(move1)
    # c_board = c_state.board
    # c_board.printBoard()
    print('next = ', next_move)
    print(c_board.boardValues)
    board_state = GameState(state=c_board, next_to_move=next_move)
    root = MonteCarloTreeSearchNode(state=board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(100)
    c_state = best_node.state
    c_board = c_state.board
    c_board.printBoard()
    # graphics(c_board)
    next_move = -1 * next_move

    if c_state.is_game_over():
        break

print("Koniec")
