import numpy as np
import Pieces


#       tipe  value
# pawn   1     1
# horse  2     5
# bishop 3     8
# tower  4     10
# queen  5     20
# king   6     1000


class Board:

    def __init__(self):
        self.board = None
        self.position = {}
        self.pieces = {}

    def initGame(self):
        self.board = np.array(
            [[4, 2, 3, 5, 6, 3, 2, 4],  # 0
             [1, 1, 1, 1, 1, 1, 1, 1],  # 1
             [0, 0, 0, 0, 0, 0, 0, 0],  # 2
             [0, 0, 0, 0, 0, 0, 0, 0],  # 3
             [0, 0, 0, 0, 0, 0, 0, 0],  # 4
             [0, 0, 0, 0, 0, 0, 0, 0],  # 5
             [1, 1, 1, 1, 1, 1, 1, 1],  # 6
             [4, 2, 3, 5, 6, 3, 2, 4]]  # 7
            # 0  1  2  3  4  5  6  7
        )
        self.board = self.board.transpose()

        self.setPieces(0, 1, 0, 1)
        self.setPieces(1, 6, 7, -1)

        for item in self.position.items():
            self.pieces[item[1]] = item[0]

    def getMoves(self, player):
        moves = []
        pieces = self.position.keys()
        for piece in pieces:
            if piece.player == player:
                moves += (piece.move(), piece.tipe)

        return moves

    def getActualPieces(self, player):
        pieces = []

        for piece in self.position.keys():
            if piece.player == player:
                pieces.append(piece)

        return pieces

    def promotions(self, piece, coord, tipe):
        self.position.pop(piece)
        self.pieces.pop(coord)
        self.board[coord[0]][coord[1]] = tipe

        newPiece = None

        if tipe == 5:
            newPiece = Pieces.Queen(piece.player, self)
        if tipe == 2:
            newPiece = Pieces.Horse(piece.player, self)
        if tipe == 3:
            newPiece = Pieces.Bishop(piece.player, self)
        if tipe == 4:
            newPiece = Pieces.Tower(piece.player, self)

        self.pieces[coord] = newPiece
        self.position[newPiece] = coord

    def movePiece(self, piece, coord):
        if coord[0] == 9:      # Promotions
            self.promotions(piece, self.position[piece], coord[1])
            return 0

        self.board[coord[0]][coord[1]] = piece.tipe
        if piece.tipe == 1 or piece.tipe == 4 or piece.tipe == 6:  # New pieces
            piece.notNew()

        x, y = self.position[piece]
        self.board[x][y] = 0

        self.position[piece] = coord

        if coord in self.pieces:
            capturePiece = self.pieces[coord]

            self.position.pop(capturePiece)
            if capturePiece.tipe == 6:
                return 1  # End play

        self.pieces[coord] = piece
        self.pieces.pop((x, y))

        return 0  # continue

    def setPieces(self, player, f1, f2, direction):

        self.position[Pieces.Pawn(player, self, direction)] = (0, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (1, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (2, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (3, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (4, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (5, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (6, f1)
        self.position[Pieces.Pawn(player, self, direction)] = (7, f1)

        self.position[Pieces.Tower (player, self)] = (0, f2)
        self.position[Pieces.Horse (player, self)] = (1, f2)
        self.position[Pieces.Bishop(player, self)] = (2, f2)
        self.position[Pieces.Queen (player, self)] = (3, f2)
        self.position[Pieces.King  (player, self)] = (4, f2)
        self.position[Pieces.Bishop(player, self)] = (5, f2)
        self.position[Pieces.Horse (player, self)] = (6, f2)
        self.position[Pieces.Tower (player, self)] = (7, f2)

    def movePawn(self, pawn, direction):
        moves = []
        x, y = self.position[pawn]
        # Moves

        if 0 <= y + direction < 8 and self.board[x][y + direction] == 0:

            moves.append((x, y + direction))
            if pawn.new and self.board[x][y + (2 * direction)] == 0:
                moves.append((x, y + (2 * direction)))

        # Promotions

        if y == 7:
            moves.append((9, 2))  # horse
            moves.append((9, 3))  # Bishop
            moves.append((9, 4))  # tower
            moves.append((9, 5))  # queen

            # Captures

        if 0 <= y + direction < 8 and 8 > x - 1 >= 0 and self.board[x - 1][y + direction] != 0 and \
                (not((x - 1, y + direction) in self.pieces) or pawn.player != self.pieces[(x - 1, y + direction)].player):
            moves.append((x - 1, y + direction))

        if 0 <= y + direction < 8 and 0 <= x + 1 < 8 and self.board[x + 1][y + direction] != 0 and \
                (not((x + 1, y + direction) in self.pieces) or pawn.player != self.pieces[(x + 1, y + direction)].player):
            moves.append((x + 1, y + direction))

        return moves

    def moveHorse(self, horse):
        moves = []
        x, y = self.position[horse]

        if x + 2 < 8 and y + 1 < 8 and (not((x + 2, y + 1) in self.pieces) or horse.player != self.pieces[(x + 2, y + 1)].player):
            moves.append((x + 2, y + 1))

        if x + 2 < 8 and y - 1 >= 0 and (not((x + 2, y - 1) in self.pieces) or horse.player != self.pieces[(x + 2, y - 1)].player):
            moves.append((x + 2, y - 1))

        if x - 2 >= 0 and y + 1 < 8 and (not((x - 2, y + 1) in self.pieces) or horse.player != self.pieces[(x - 2, y + 1)].player):
            moves.append((x - 2, y + 1))

        if x - 2 >= 0 and y - 1 >= 0 and (not((x - 2, y - 1) in self.pieces) or horse.player != self.pieces[(x - 2, y - 1)].player):
            moves.append((x - 2, y - 1))

        if x + 1 < 8 and y + 2 < 8 and (not((x + 1, y + 2) in self.pieces) or horse.player != self.pieces[(x + 1, y + 2)].player):
            moves.append((x + 1, y + 2))

        if x - 1 >= 0 and y + 2 < 8 and (not((x - 1, y + 2) in self.pieces) or horse.player != self.pieces[(x - 1, y + 2)].player):
            moves.append((x - 1, y + 2))

        if x + 1 < 8 and y - 2 >= 0 and (not((x + 1, y - 2) in self.pieces) or horse.player != self.pieces[(x + 1, y - 2)].player):
            moves.append((x + 1, y - 2))

        if x - 1 >= 0 and y - 2 >= 0 and (not((x - 1, y - 2) in self.pieces) or horse.player != self.pieces[(x - 1, y - 2)].player):
            moves.append((x - 1, y - 2))

        return moves

    def checkDirection(self, piece, stepX, stepY):
        moves = []
        x, y = self.position[piece]

        while (0 <= x + stepX < 8) and (0 <= y + stepY < 8):
            x += stepX
            y += stepY

            if self.board[x][y] != 0:
                if (x, y) in self.pieces and piece.player != self.pieces[(x, y)].player:
                    moves.append((x, y))
                break
            else:
                moves.append((x, y))


        return moves

    def moveBishop(self, bishop):
        moves = []

        moves += self.checkDirection(bishop, -1, 1)
        moves += self.checkDirection(bishop,  1, 1)
        moves += self.checkDirection(bishop,  1, -1)
        moves += self.checkDirection(bishop, -1, -1)

        return moves

    def moveTower(self, tower):
        moves = []

        moves += self.checkDirection(tower, -1, 0)
        moves += self.checkDirection(tower,  1, 0)
        moves += self.checkDirection(tower,  0, -1)
        moves += self.checkDirection(tower,  0,  1)

        return moves

    def moveQueen(self, queen):
        moves = self.moveBishop(queen) + self.moveTower(queen)
        return moves

    def moveKing(self, king):
        moves = []
        x, y = self.position[king]

        if x + 1 < 8 and (not((x + 1, y) in self.pieces) or king.player != self.pieces[(x + 1, y)].player):
            moves.append((x + 1, y))

        if x - 1 >= 0 and (not((x - 1, y) in self.pieces) or king.player != self.pieces[(x - 1, y)].player):
            moves.append((x - 1, y))

        if y + 1 < 8 and (not((x, y + 1) in self.pieces) or king.player != self.pieces[(x, y + 1)].player):
            moves.append((x, y + 1))

        if y - 1 >= 0 and (not((x, y - 1) in self.pieces) or king.player != self.pieces[(x, y - 1)].player):
            moves.append((x, y - 1))

        if x + 1 < 8 and y + 1 < 8 and (not((x + 1, y + 1) in self.pieces) or king.player != self.pieces[(x + 1, y + 1)].player):
            moves.append((x + 1, y + 1))

        if x - 1 >= 0 and y - 1 >= 0 and (not((x - 1, y - 1) in self.pieces) or king.player != self.pieces[(x - 1, y - 1)].player):
            moves.append((x - 1, y - 1))

        if x - 1 >= 0 and y + 1 < 8 and (not((x - 1, y + 1) in self.pieces) or king.player != self.pieces[(x - 1, y + 1)].player):
            moves.append((x - 1, y + 1))

        if x + 1 < 8 and y - 1 >= 0 and (not((x + 1, y - 1) in self.pieces) or king.player != self.pieces[(x + 1, y - 1)].player):
            moves.append((x + 1, y - 1))

        if king.new:
            xd = x
            while xd + 1 < 8:
                xd += 1
                if self.board[xd][y] == 0:
                    continue

                if self.board[xd][y] != 4:
                    break

                if self.pieces[(xd, y)].new:
                    moves.append((xd, y))

            xd = x
            while xd - 1 < 8:
                xd -= 1
                if self.board[xd][y] == 0:
                    continue

                if self.board[xd][y] != 4:
                    break

                if self.pieces[(xd, y)].new:
                    moves.append((xd, y))

        return moves
