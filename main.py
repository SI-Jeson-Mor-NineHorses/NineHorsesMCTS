import pygame
import sys
from GUI.board_gui import *
from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from state import GameState
from state import GameMove
from position import Position
from board import *

pygame.init()
pygame.font.init()

# Ustawienia okna gry
screen = pygame.display.set_mode((60*9, 60 * 9))
pygame.display.set_caption('Python Jeson Mor Game')
clock = pygame.time.Clock()  # odświeżanie okna

# Załadowanie wygerowanej planszy
bg = pygame.image.load("./assets/board.png").convert()
player = 1

board = BoardGUI()

global all_sprites_list, sprites
all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]
all_sprites_list.add(sprites)


def reload_sprites():
    return [piece for row in board.array for piece in row if piece]


def select_piece_xy(color, x, y):
    # get a list of all sprites that are under the mouse cursor
    # lista wszystkich duszków, ktore sa pod kursorem myszy
    clicked_sprites = [s for s in sprites if s.x == x and s.y == y]

    # podświetla i zwaraca jeśli jest to pionek gracza
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]
    elif len(clicked_sprites) == 1:
        return clicked_sprites[0]

def select_piece(color):
    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    # lista wszystkich duszków, ktore sa pod kursorem myszy
    clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    # podświetla i zwaraca jeśli jest to pionek gracza
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]
    elif len(clicked_sprites) == 1:
        return clicked_sprites[0]

def select_square():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return y, x

# mode:
# 0 - gracz vs gracz
# 1 - gracz vs komputer
# 2 - komputer vs komputer+

def run_game(mode, number_of_simulations):
    global sprites
    gameover = False # flaga końca gry
    winner = "" # identyfikator zwycięzcy
    selected = False
    trans_table = dict()
    checkWhite = False
    player = 1

    previous_move = ''
    current_move = ''
    run_flag = 0

    screen.blit(bg, (0, 0))
    all_sprites_list.draw(screen)
    pygame.display.update()
    clock.tick(60)

    while not gameover:
        previous_move = current_move
        if player == 1:
            if mode == 0 or mode == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    # wybór pionka do wykonania ruchu
                    elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                        board.unhighlight_optional_moves()
                        piece = select_piece("w")

                        # generuje "legalne" ruchy pionka
                        if piece != Empty and piece.color == "w":
                            # sprawdzenie dostępnych ruchów
                            player_moves = piece.gen_legal_moves(board)
                            # all_player_moves = board.get_all_legal_moves("w")

                            # podświetlenie dostępnych ruchów
                            board.highlight_optional_moves(player_moves)
                            selected = True

                    # pionek wybrany -> wybór ruchu
                    elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                        board.unhighlight_optional_moves()
                        square = select_square()

                        # sprawdza czy wybrane pole jest w zasięgu dozwolonych ruchów
                        if square in player_moves:
                            oldx = piece.x
                            oldy = piece.y
                            dest = board.array[square[0]][square[1]]

                            # wykonanie ruchu
                            board.move_piece(piece, square[0], square[1])

                            if dest:  # aktualizacja 'duszków' względem stanu planszy
                                sprites = reload_sprites()
                                all_sprites_list.empty()
                                all_sprites_list.add(sprites)

                            selected = False
                            player = 2

                        # anuluje ruch, jezeli wybrane zostalo to samo pole
                        elif (piece.y, piece.x) == square:
                            piece.unhighlight()
                            selected = False

                        # ruch jest nieważny
                        else:
                            pygame.display.update()
                            # board.highlight_optional_moves(player_moves)
                            pygame.time.wait(1000)
            elif mode == 2:
                board_mcts = Board(board=simplify_board(board.array))
                board_state = GameState(state=board_mcts, next_to_move=1)
                root = MonteCarloTreeSearchNode(state=board_state, parent=None)
                mcts = MonteCarloTreeSearch(root)
                best_node = mcts.best_action(number_of_simulations)
                c_state = best_node.state
                c_board = c_state.board

                x_from = c_state.current_move.pos_from.getX()
                y_from = c_state.current_move.pos_from.getY()
                # print("x_from", x_from)
                # print("y_from", y_from)

                x_to = c_state.current_move.pos_to.getX()
                y_to = c_state.current_move.pos_to.getY()
                # print("x_to", x_to)
                # print("y_to", y_to)



                piece = select_piece_xy("w", x_from, y_from)
                square = (x_to, y_to)
                dest = board.array[y_to][x_to]

                board.move_piece(piece, y_to, x_to)  # wykonanie ruchu
                if dest:
                    sprites = reload_sprites()
                    all_sprites_list.empty()
                    all_sprites_list.add(reload_sprites())
                player = 2

        # drugi gracz
        elif player == 2:
            if mode == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                        board.unhighlight_optional_moves()
                        piece = select_piece("b")

                        if piece != Empty and piece.color == "b":
                            # sprawdzenie dostępnych ruchów
                            player_moves = piece.gen_legal_moves(board)
                            # print(player_moves)
                            # podświetlenie dostępnych ruchów
                            board.highlight_optional_moves(player_moves)
                            selected = True

                    elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                        board.unhighlight_optional_moves()
                        square = select_square()

                        if square in player_moves:
                            oldx = piece.x
                            oldy = piece.y
                            dest = board.array[square[0]][square[1]]

                            # wykonanie ruchu
                            board.move_piece(piece, square[0], square[1])
                            if dest:
                                sprites = reload_sprites()
                                all_sprites_list.empty()
                                all_sprites_list.add(reload_sprites())

                            selected = False
                            player = 1

                        elif (piece.y, piece.x) == square:
                            piece.unhighlight()
                            selected = False
                        else:
                            pygame.display.update()
                            board.highlight_optional_moves(player_moves)
                            pygame.time.wait(1000)

            elif mode == 1:
                board_mcts = Board(board=simplify_board(board.array))
                print(board_mcts.boardValues)
                board_state = GameState(state=board_mcts, next_to_move=-1)
                root = MonteCarloTreeSearchNode(state=board_state, parent=None)
                mcts = MonteCarloTreeSearch(root)
                best_node = mcts.best_action(number_of_simulations)
                c_state = best_node.state
                c_board = c_state.board

                x_from = c_state.current_move.pos_from.getX()
                y_from = c_state.current_move.pos_from.getY()
                # print("x_from", x_from)
                # print("y_from", y_from)

                x_to = c_state.current_move.pos_to.getX()
                y_to = c_state.current_move.pos_to.getY()
                # print("x_to", x_to)
                # print("y_to", y_to)



                piece = select_piece_xy("b", x_from, y_from)
                square = (x_to, y_to)
                dest = board.array[y_to][x_to]

                board.move_piece(piece, y_to, x_to)  # wykonanie ruchu
                if dest:
                    sprites = reload_sprites()
                    all_sprites_list.empty()
                    all_sprites_list.add(reload_sprites())
                player = 1

            elif mode == 2:
                board_mcts = Board(board=simplify_board(board.array))
                board_state = GameState(state=board_mcts, next_to_move=-1)
                root = MonteCarloTreeSearchNode(state=board_state, parent=None)
                mcts = MonteCarloTreeSearch(root)
                best_node = mcts.best_action(number_of_simulations)
                c_state = best_node.state
                c_board = c_state.board

                x_from = c_state.current_move.pos_from.getX()
                y_from = c_state.current_move.pos_from.getY()
                # print("x_from", x_from)
                # print("y_from", y_from)

                x_to = c_state.current_move.pos_to.getX()
                y_to = c_state.current_move.pos_to.getY()
                # print("x_to", x_to)
                # print("y_to", y_to)

                piece = select_piece_xy("b", x_from, y_from)
                square = (x_to, y_to)
                dest = board.array[y_to][x_to]

                board.move_piece(piece, y_to, x_to)  # wykonanie ruchu
                if dest:
                    sprites = reload_sprites()
                    all_sprites_list.empty()
                    all_sprites_list.add(reload_sprites())
                player = 1

        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)

        arr = []
        for j in range(9):
            for piecee in board.array[j]:
                arr.append(piecee.color + piecee.symbol)

        # check end game
        if 'wN' not in arr:
            gameover = True
            winner = "Black"
        elif 'bN' not in arr:
            gameover = True
            winner = "White"

        current_move = arr[40]
        if previous_move == 'wN' and current_move == "_N":
            gameover = True
            winner = "White"
        elif previous_move == 'bN' and current_move == "_N":
            gameover = True
            winner = "Black"

        output_board = simplify_board(board.array)


    print("Wygrał: ", winner)

def printBoard(boardValues):
    for j in range(9):
        arr = []
        for i in range(9):
            x = boardValues[j][i]
            if x is not None:
                arr.append(x)
            else:
                arr.append("_")
        print(arr)

if __name__ == "__main__":
    run_game(2, 100)