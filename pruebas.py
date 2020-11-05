import Board


board = Board.Board()

board.initGame()

moves = board.getMoves(1)

piecesPlayerBlue = board.getActualPieces(1)

print(moves)

print(board.board)

print(piecesPlayerBlue)

board.movePiece(piecesPlayerBlue[0], (0, 4))


moves = board.getMoves(1)

piecesPlayerBlue = board.getActualPieces(1)

print(moves)

print(board.board)

print(piecesPlayerBlue)



board.movePiece(piecesPlayerBlue[0], (0, 3))
print(board.board)
board.movePiece(piecesPlayerBlue[0], (0, 2))
print(board.board)
board.movePiece(piecesPlayerBlue[0], (1, 1))


print(board.board)
moves = board.getMoves(1)

moves1 = board.getMoves(0)

piecesPlayerBlue = board.getActualPieces(1)

print(moves)

print(moves1)
print(board.board)

print(piecesPlayerBlue)


