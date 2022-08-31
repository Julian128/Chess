
class Move():

    # key : value
    # translates to proper chess notation

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {i: j for j, i in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {i: j for j, i in filesToCols.items()}



    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.evaluation = 0
        self.check = False
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000, self.startCol * 100 + self.endRow * 10 + self.endCol

        self.isPawnPromotion = self.pieceMoved == "wP" and self.endRow == 0 or self.pieceMoved == "bP" and self.endRow == 7

        self.isEnpassantMove = self.pieceMoved[1] == "P" and abs(self.startRow - self.endRow) == 1 and abs(self.startCol - self.endCol) == 1 and self.pieceCaptured == "--"

        if self.isEnpassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
        self.isCastleMove = self.pieceMoved[1] == "K" and abs(self.startCol - self.endCol) == 2


    def __eq__(self, other):  # needed to allow getAllPossibleMoves() method
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
