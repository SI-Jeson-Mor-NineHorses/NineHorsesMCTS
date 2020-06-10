class Position:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __repr__(self):
        return "(%s, %s)" % (self.y, self.x)

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y
