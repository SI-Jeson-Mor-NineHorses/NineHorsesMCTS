from PIL import Image, ImageDraw
from itertools import cycle

# Funkcja wykorzystywan do utworzenia planszy gry

def draw_chessboard(n=9, pixel_width=60 * 9):

    def sq_start(i):
        return i * pixel_width / n

    def square(i, j):
        return list(map(sq_start, [i, j, i + 1, j + 1]))

    image = Image.new("RGB", (pixel_width, pixel_width), (250, 206, 165))
    draw_square = ImageDraw.Draw(image).rectangle
    squares = (square(i, j)
               for i_start, j in zip(cycle((0, 1)), list(range(n)))
               for i in range(i_start, n, 2))
    i = 0
    for sq in squares:
        draw_square(sq, fill='#d18e4f')
        i = i+1
        if i==21:
            draw_square(sq, fill='#734317')
    squares = (square(i, j)
               for i_start, j in zip(cycle((0, 1)), list(range(n)))
               for i in range(i_start, n, 2))
    image.save("board.png")

draw_chessboard(9)
