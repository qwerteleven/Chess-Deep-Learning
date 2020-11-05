#       tipe  value
# pawn   1     1
# horse  2     5
# bishop 3     8
# tower  4     10
# queen  5     20
# king   6     1000

# where are my Interfaces?


class Pawn:

    def __init__(self, player, board, direction):
        self.tipe = 1
        self.new = True
        self.canMove = True
        self.player = player
        self.capture = False
        self.board = board
        self.direction = direction

    def move(self):  # because only move in one direction
        return self.board.movePawn(self, self.direction)

    def capture(self):
        self.capture = True

    def canMove(self, state):
        self.canMove = state

    def notNew(self):
        self.new = False


class Horse:

    def __init__(self, player, board):
        self.tipe = 2
        self.canMove = True
        self.player = player
        self.capture = False
        self.board = board

    def move(self):
        return self.board.moveHorse(self)

    def capture(self):
        self.capture = True

    def canMove(self, state):
        self.canMove = state


class Bishop:

    def __init__(self, player, board):
        self.tipe = 3
        self.canMove = False
        self.player = player
        self.capture = False
        self.board = board

    def move(self):
        return self.board.moveBishop(self)

    def capture(self):
        self.capture = True

    def canMove(self, state):
        self.canMove = state


class Tower:

    def __init__(self, player, board):
        self.tipe = 4
        self.new = True
        self.canMove = False
        self.player = player
        self.capture = False
        self.board = board

    def move(self):
        return self.board.moveTower(self)

    def capture(self):
        self.capture = True

    def canMove(self, state):
        self.canMove = state

    def notNew(self):
        self.new = False


class Queen:

    def __init__(self, player, board):
        self.tipe = 5
        self.canMove = False
        self.player = player
        self.capture = False
        self.board = board

    def move(self):
        return self.board.moveQueen(self)

    def capture(self):
        self.capture = True

    def canMove(self, state):
        self.canMove = state


class King:

    def __init__(self, player, board):
        self.tipe = 6
        self.new = True
        self.canMove = False
        self.player = player
        self.capture = False
        self.board = board

    def move(self):
        return self.board.moveKing(self)

    def capture(self):
        self.capture = True

    def canMove(self, state):
        self.canMove = state

    def notNew(self):
        self.new = False
