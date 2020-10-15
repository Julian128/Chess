

class GameState():
    def __init__(self):  # board is 8x8 2D list, b = black, w = white

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        self.moveFunctions = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}  # maps letter of piece to movefunction of piece, this is a dictionary

        self.whiteToMove = True
        self.whiteCastleAllowed = True
        self.blackCastleAllowed = True
        self.moveLog = []
        self.checkMate = False
        self.staleMate = False

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        #self.undoneMove = ()



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            print("whiteKingMoved: " + str(move.getChessNotation()))
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            print("blackKingMoved: " + str(move.getChessNotation()))
            self.blackKingLocation = (move.endRow, move.endCol)


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            #self.undoneMove = move
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            print("whiteKingMoved: " + str(move.getChessNotation()))
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            print("blackKingMoved: " + str(move.getChessNotation()))
            self.blackKingLocation = (move.startRow, move.startCol)

 #   def redomove(self):
  #      move = self.undonemove
   #     self.board[move.startrow][move.startcol] = move.piececaptured
    #    self.board[move.endrow][move.endcol] = move.piecemoved
     #   self.whitetomove = not self.whitetomove



    def getValidMoves(self):
        moves = self.getAllPossibleMoves()

        for i in range(len(moves) - 1, 0, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

            if len(moves) == 0:  # either checkmate or stalemate
                if self.inCheck():
                    self.checkMate = True
                else:
                    self.staleMate = True
            else:
                self.checkMate = False
                self.staleMate = False

        return moves


    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove

        for move in opponentMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls appropriate move function
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":  # one square pawn push
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c >= 1:  # pawn capture to the left
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

            if c <= 6:  # pawn capture to the right
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r + 1][c] == "--":  # one square pawn push
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c >= 1:  # pawn capture to the left
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c <= 6:  # pawn capture to the right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    def getRookMoves(self, r, c, moves):
        rookMoves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if self.whiteToMove:
            enemyColour = "b"
        else:
            enemyColour = "w"

        for i in rookMoves:
            for j in range(1, 8):
                endRow = r + j * i[0]
                endCol = c + j * i[1]

                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board[endRow][endCol][0] == enemyColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # no more moves behind enemy piece
                    else:
                        break  # no more moves behind ally piece

                else:
                    break




    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        if self.whiteToMove:
            allyColour = "w"
        else:
            allyColour = "b"

        for i in knightMoves:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endSq = self.board[endRow][endCol]
                if endSq[0] != allyColour:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



    def getBishopMoves(self, r, c, moves):
        bishopMoves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        if self.whiteToMove:
            enemyColour = "b"
        else:
            enemyColour = "w"

        for i in bishopMoves:
            for j in range(1, 8):
                endRow = r + j * i[0]
                endCol = c + j * i[1]

                if  0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif self.board[endRow][endCol][0] == enemyColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
    
                        break  # no more moves behind enemy piece
                    else:
                        break  # no more moves behind ally piece

                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, -1)]
        if self.whiteToMove:
            allyColour = "w"
        else:
            allyColour = "b"

        for i in kingMoves:
            endRow = r + i[0]
            endCol = c + i[1]

            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if self.board[endRow][endCol][0] != allyColour:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {i: j for j, i in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {i: j for j, i in filesToCols.items()}





    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000, self.startCol * 100 + self.endRow * 10 + self.endCol  # unique moveID for every possible move in a boardstate


    def __eq__(self, other):  # needed to allow getAllPossibleMoves() method
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return false

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]