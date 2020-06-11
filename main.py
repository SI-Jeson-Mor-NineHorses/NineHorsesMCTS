import pygame
import sys
from GUI.board_gui import *
from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from state import GameState
from state import GameMove
from position import Position
from board import *
import pygame_textinput
import re
import time

pygame.init()
pygame.font.init()

# Ustawienia okna gry
screen = pygame.display.set_mode((60*9, 60 * 9))
pygame.display.set_caption('Python Jeson Mor Game')
clock = pygame.time.Clock()  # odświeżanie okna

#MENU
menu_image = pygame.image.load("./assets/gui/home-screen.png")
button_image = pygame.image.load("./assets/gui/button.png")
button_image_small = pygame.image.load("./assets/gui/small-button.png")
settings_image = pygame.image.load("./assets/gui/settings.png")
mode_image = pygame.image.load("./assets/gui/mode.png")

winner_white = pygame.image.load("./assets/gui/white_winner.png")
winner_black = pygame.image.load("./assets/gui/black_winner.png")

#MENU TEXT
text_color = (124, 73, 0)
highlight_color = (140, 97, 72)
menu_font = pygame.font.Font("./assets/gui/GROBOLD.ttf", 20)
menu_font_small = pygame.font.Font("./assets/gui/GROBOLD.ttf", 15)

start_game_text = menu_font.render("Start game", True, text_color)
settings_text = menu_font.render("Settings", True, text_color)
quit_text = menu_font.render("Quit", True, text_color)
accept_text = menu_font.render("Accept", True, text_color)
back_text = menu_font_small.render("Back", True, text_color)

player_vs_player_text = menu_font.render("Player vs Player", True, text_color)
player_vs_ai_text = menu_font.render("Player vs AI", True, text_color)
ai_vs_ai_text = menu_font.render("AI vs AI", True, text_color)


textinput_font = pygame.font.Font("./assets/gui/GROBOLD.ttf", 22)

# Załadowanie wygenerowanej planszy
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
    global all_sprites_list, sprites
    global board

    board = BoardGUI()
    all_sprites_list = pygame.sprite.Group()
    sprites = [piece for row in board.array for piece in row if piece]
    all_sprites_list.add(sprites)

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

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameover = True

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

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameover = True

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

            elif mode == 1 or mode == 2:
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
    if winner == "White":
        screen.blit(winner_white, (0, 0))
        pygame.display.update()
        time.sleep(5)
    elif winner == "Black":
        screen.blit(winner_black, (0, 0))
        pygame.display.update()
        time.sleep(5)


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
#    run_game(1, 1000)
    number_of_simulations = 1000
    menu = True
    while True:
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    print(x, y)
                    if button_image.get_rect(topleft=(164, 140)).collidepoint(x, y):
                        print("start game")
                        mode = True
                        while mode:
                            events = pygame.event.get()
                            for event in events:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x, y = event.pos

                                    if button_image.get_rect(topleft=(164, 140)).collidepoint(x, y):
                                        mode = False
                                        run_game(0, number_of_simulations)
                                    elif button_image.get_rect(topleft=(164, 210)).collidepoint(x, y):
                                        mode = False
                                        run_game(1, number_of_simulations)
                                    elif button_image.get_rect(topleft=(164, 280)).collidepoint(x, y):
                                        mode = False
                                        run_game(2, number_of_simulations)
                                    elif button_image_small.get_rect(topleft=(450, 500)).collidepoint(x, y):
                                        mode = False

                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        mode = False

                                elif event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()

                            x, y = pygame.mouse.get_pos()
                            if button_image.get_rect(topleft=(164, 140)).collidepoint(x, y):
                                player_vs_player_text = menu_font.render("Player vs Player", True, highlight_color)
                            elif button_image.get_rect(topleft=(164, 210)).collidepoint(x, y):
                                player_vs_ai_text = menu_font.render("Player vs AI", True, highlight_color)
                            elif button_image.get_rect(topleft=(164, 280)).collidepoint(x, y):
                                ai_vs_ai_text = menu_font.render("AI vs AI", True, highlight_color)
                            elif button_image_small.get_rect(topleft=(450, 500)).collidepoint(x, y):
                                back_text = menu_font_small.render("Back", True, highlight_color)
                            else:
                                player_vs_player_text = menu_font.render("Player vs Player", True, text_color)
                                player_vs_ai_text = menu_font.render("Player vs AI", True, text_color)
                                ai_vs_ai_text = menu_font.render("AI vs AI", True, text_color)
                                back_text = menu_font_small.render("Back", True, text_color)

                            screen.blit(mode_image, (0, 0))
                            screen.blit(button_image, (164, 140))
                            screen.blit(player_vs_player_text, (195, 150))

                            screen.blit(button_image, (164, 210))
                            screen.blit(player_vs_ai_text, (210, 220))

                            screen.blit(button_image, (164, 280))
                            screen.blit(ai_vs_ai_text, (230, 290))

                            screen.blit(button_image_small, (450, 500))
                            screen.blit(back_text, (470, 505))

                            pygame.display.flip()
                            pygame.display.update()

                    elif button_image.get_rect(topleft=(164, 210)).collidepoint(x, y):
                        print("settings")
                        settings = True
                        textinput = pygame_textinput.TextInput(initial_string=str(number_of_simulations),
                                                               font_family="./assets/gui/GROBOLD.ttf", font_size=22,
                                                               text_color=(124, 73, 0), max_string_length=10)
                        while settings:
                            events = pygame.event.get()
                            textinput.update(events)
                            for event in events:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x, y = event.pos
                                    if button_image.get_rect(topleft=(164, 250)).collidepoint(x, y):
                                        pattern = re.compile("\d{1,10}$")
                                        if pattern.match(textinput.get_text()):
                                            textinput.set_text_color((0, 255, 0))
                                            number_of_simulations = int(textinput.get_text())
                                        else:
                                            textinput.set_text_color((255, 0, 0))
                                    elif button_image_small.get_rect(topleft=(450, 500)).collidepoint(x, y):
                                        settings = False

                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        settings = False

                                elif event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()

                            try:
                                if number_of_simulations != int(textinput.get_text()):
                                    textinput.set_text_color((124, 73, 0))
                            except:
                                pass

                            x, y = pygame.mouse.get_pos()
                            if button_image.get_rect(topleft=(164, 250)).collidepoint(x, y):
                                accept_text = menu_font.render("Accept", True, highlight_color)
                            elif button_image_small.get_rect(topleft=(450, 500)).collidepoint(x, y):
                                back_text = menu_font_small.render("Back", True, highlight_color)
                            else:
                                accept_text = menu_font.render("Accept", True, text_color)
                                back_text = menu_font_small.render("Back", True, text_color)


                            input_text_size = textinput_font.size(textinput.get_text())

                            screen.blit(settings_image, (0, 0))
                            screen.blit(button_image, (164, 250))
                            screen.blit(accept_text, (230, 260))
                            screen.blit(button_image_small, (450, 500))
                            screen.blit(back_text, (470, 505))
                            screen.blit(textinput.get_surface(), (270 - int(input_text_size[0]/2), 167))
                            pygame.display.flip()
                            pygame.display.update()


                    elif button_image.get_rect(topleft=(164, 280)).collidepoint(x, y):
                        print("exit")
                        pygame.quit()
                        quit()

            #Highlight menu text
            x, y = pygame.mouse.get_pos()
            if button_image.get_rect(topleft=(164, 140)).collidepoint(x, y):
                start_game_text = menu_font.render("Start game", True, highlight_color)
            elif button_image.get_rect(topleft=(164, 210)).collidepoint(x, y):
                settings_text = menu_font.render("Settings", True, highlight_color)
            elif button_image.get_rect(topleft=(164, 280)).collidepoint(x, y):
                quit_text = menu_font.render("Quit", True, highlight_color)
            else:
                start_game_text = menu_font.render("Start game", True, text_color)
                settings_text = menu_font.render("Settings", True, text_color)
                quit_text = menu_font.render("Quit", True, text_color)

            #Display menu
            screen.blit(menu_image, (0, 0))

            screen.blit(button_image, (164, 140))
            screen.blit(start_game_text, (215, 150))

            screen.blit(button_image, (164, 210))
            screen.blit(settings_text, (230, 220))

            screen.blit(button_image, (164, 280))
            screen.blit(quit_text, (245, 290))

            pygame.display.flip()
            clock.tick(60)
            pygame.display.update()
