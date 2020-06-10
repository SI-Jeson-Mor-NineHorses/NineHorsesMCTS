
class Board:
    boardValues = []
    totalMoves = 0
    IN_PROGRESS = -1
    DRAW = 0
    P1 = 1
    P2 = -1

    def __init__(self, board=None, boardSize=None, boardValues=None, totalMoves=None):
        self.WINNER = 0
        if board is not None:
            self.boardValues = board

        elif boardSize is not None:
            self.boardValues = [
                [-1 for i in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [1 for i in range(9)],
            ]
        elif boardValues is not None and totalMoves is not None:
            self.boardValues = boardValues
            self.totalMoves = totalMoves

        else:
            self.boardValues = [
                [-1 for i in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [0 for x in range(9)],
                [1 for i in range(9)],
            ]

    def performMove(self, player, pos1, pos2):
        self.totalMoves += 1
        if pos1.getX() == 4 and pos1.getY() == 4:
            self.WINNER = player
        self.boardValues[pos1.getY()][pos1.getX()] = 0
        self.boardValues[pos2.getY()][pos2.getX()] = player

    def getBoardValues(self):
        return self.boardValues

    def setBoardValues(self, boardValues):
        self.boardValues = boardValues

    def checkStatus(self):
        arr = []
        for j in range(9):
            for i in self.boardValues[j]:
                arr.append(i)

        if 1 not in arr:
            return Board.P2
        elif -1 not in arr:
            return Board.P1
        elif self.WINNER != 0:
            return self.WINNER
        else:
            return 2

    def printBoard(self):
        for j in range(9):
            arr = []
            for i in range(9):
                x = self.boardValues[j][i]
                if x is not None:
                    arr.append(x)
                else:
                    arr.append("--")
            print(arr)

    def getPossibleMoves(self, player):
        moves_list = []
        for j in range(9):
            for i in range(9):
                p = self.boardValues[j][i]
                if p == player:
                    for move in self.gen_legal_moves(p, j, i):
                        moves_list.append({player: {'from': (j, i), 'to': move}})
        return moves_list

    # nine horses logic
    def gen_legal_moves(self, player, y, x):
        move_set = set()
        offsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

        for offset in offsets:
            newX = x + offset[0]
            newY = y + offset[1]

            if self.move_check(player, newY, newX):
                move_set.add((newY, newX))
        return move_set

    # nine horses logic
    def move_check(self, player, y, x):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return False
        piece = self.boardValues[y][x]
        if piece == 0:
            return True
        else:
            if piece != player:
                return True
            else:
                return False

    def printStatus(self):
        status = self.checkStatus()
        if status == 1:
            print("Player 1 wins")
        elif status == 2:
            print("Player 2 wins")
        elif status == 0:
            print("Game Draw")
        else:
            print("Game In Progress")
