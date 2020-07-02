import pygame
import os
import sys

# def capture_check(your_color, y, x, board):
#     piece = board.array[y][x]
#     if piece == None:
#         return False
#     else:
#         if piece.color != your_color:
#             return True
#         else:
#             return False

# Sprawdza czy wykonanie ruchu jest możliwe


def resource_path(relative_path):
    default = "assets/"
    relative_path = default + relative_path
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def move_check(your_color, y, x, board):
    if x < 0 or x > 8 or y < 0 or y > 8:
        return False
    piece = board.array[y][x]
    if piece.color == 'x':
        return True
    else:
        if piece.color != your_color:
            return True
        else:
            return False

class Piece(pygame.sprite.Sprite):

    def __init__(self, color, rgb, y, x):
        super().__init__()
        self.color = color
        self.rgb =rgb

        # pozycja na macierzy planszy
        self.x = x
        self.y = y

        # pozwala na przezroczystość tła figury
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        # pozycja na planszy
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, y * 60

        self.highlighed = False

    # podświetlenie wybranej figury na planszy
    def highlight(self):
        pygame.draw.rect(self.image, self.rgb, (0, 0, 60, 60),  5)
        self.highlighed = not self.highlighed

    def unhighlight(self):
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.blit(self.sprite, (0, 0))
        self.highlighed = not self.highlighed

class Knight(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,(255, 0, 0), y, x)
        self.sprite = pygame.image.load(
            resource_path("{}knight.png".format(self.color)))
        self.symbol = "N"
        self.image.blit(self.sprite, (0, 0))

    # Generowanie możliwych ruchów
    def gen_legal_moves(self, board):
        move_set = set()
        offsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color, newY, newX, board):
                move_set.add((newY, newX))
        return move_set


class Empty(Piece):
    def __init__(self, color,  y, x):
        super().__init__(color, (0, 200, 0), y, x)
        self.sprite = pygame.image.load(
            resource_path("{}knight.png".format(self.color)))
        self.symbol = "N"
        self.image.blit(self.sprite, (0, 0))

