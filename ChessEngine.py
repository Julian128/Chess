

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

        self.currentCastlingRight =  CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

        self.moveLog = []
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()  # coordinates for square where enpassant is possible

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        #self.undoneMove = ()

        #self.inCheck = False
        #self.pins = []
        #self.checks = []


    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # update kings positions
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        
        # enpassant move, if pawn moves two squares, pawn can capture enpassant
        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:  # only two square pawn pushes valid
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        if move.isEnpassantMove:
            #print("ENPASSANT")
            self.board[move.startRow][move.endCol] = "--"

        if move.isPawnPromotion:
            #print("PROMOTION")
            promotedPiece = "Q"
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        if move.isCastleMove:  # castling
            #print("CASTLE")
            if move.endCol - move.startCol == 2:  # kingside
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:  # queenside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            #self.undoneMove = move
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnpassantMove:  # undo an enpassant move
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo castling rights
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:  # queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"


    def getValidMoves(self):


        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)

        moves = self.getAllPossibleMoves()  # generate all possible moves

        for i in range(len(moves) - 1, -1, -1):  # going backwards through list
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

            if len(moves) == 0:  # either checkmate or stalemate
                if self.inCheck:
                    self.checkMate = True
                else:
                    self.staleMate = True

            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
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
                if r == 6 and self.board[r - 2][c] == "--":  # two square pawn push
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c >= 1:  # pawn capture to the left
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                    #self.board[r][c - 1] = "--"
            if c <= 6:  # pawn capture to the right
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    #self.board[r][c + 1] = "--"
           # for i in range(0, 8):  # promotion
               #if self.board[0][i] == "wP":
                  # self.board[0][i] = "wQ"

            
        else:  # black pawns
            if self.board[r + 1][c] == "--":  # one square pawn push
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c >= 1:  # pawn capture to the left
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                    #self.board[r][c - 1] = "--"
            if c <= 6:  # pawn capture to the right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    #self.board[r][c + 1] = "--"
            #for i in range(0, 8):  # promotion
                #if self.board[7][i] == "bP":
                    #self.board[7][i] = "bQ"



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
        kingMoves = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
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



        #castling  

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                if move.startCol == 7:
                    self.currentCastlingRight.bks = False

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # cant castle while in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)



    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs




class Move():

    # key : value
    # translates to proper chess notation

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {i: j for j, i in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {i: j for j, i in filesToCols.items()}





    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000, self.startCol * 100 + self.endRow * 10 + self.endCol  # unique moveID for every possible move in a boardstate

        self.isPawnPromotion = (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)


        self.isEnpassantMove = (self.pieceMoved[1] == "P" and abs(self.startRow - self.endRow) == 1 and abs(self.startCol - self.endCol) == 1 and self.pieceCaptured == "--")  # manual fix for optional parameters
        if self.isEnpassantMove:

            if self.pieceMoved == "bP":
                self.pieceCaptured = "wP"
            else:
                self.pieceCaptured = "bP"

        self.isCastleMove = (self.pieceMoved[1] == "K" and abs(self.startCol - self.endCol) == 2)


    def __eq__(self, other):  # needed to allow getAllPossibleMoves() method
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return false

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    

class Engine():
    pass