import numpy as np
import random
import time
from multiprocessing import Pool

class ChessEngine():
    def __init__(self, gs):
        self.gs = gs

    @classmethod
    def evaluation(cls, gs, whitesMove):
        gs.nodes += 1

        pawnValue = [
            [9, 9, 9, 9, 9, 9, 9, 9],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [3.5, 3, 3, 3, 3, 3, 3, 2.5],
            [1.5, 1.7, 1.8, 2, 2, 1.8, 1.7, 1.5],
            [1.1, 1.2, 1.3, 1.4, 1.4, 1.3, 1.2, 1.1],
            [1, 1.2, 1.3, 1.3, 1.3, 1.3, 1.2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0]
            ]
        knightValue = [
            [2, 2.8, 3.1, 3.1, 3.1, 3.1, 2.8, 2],
            [2.3, 2.8, 3.4, 3.4, 3.4, 3.4, 2.8, 2.3],
            [2.3, 2.8, 3.4, 3.4, 3.4, 3.4, 2.8, 2.3],
            [2.3, 2.8, 3.1, 3.1, 3.1, 3.1, 2.8, 2.3],
            [2.3, 2.8, 3.1, 3.1, 3.1, 3.1, 2.8, 2.3],
            [2.3, 2.8, 3.1, 3.1, 3.1, 3.1, 2.8, 2.3],
            [2.3, 2.8, 3.1, 3.1, 3.1, 3.1, 2.8, 2.3],
            [2.3, 2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.3]
            ]
        bishopValue = [
            [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5],
            [3.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 3.5],
            [3.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 3.5],
            [3.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 3.5],
            [3.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 3.5],
            [3.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 3.5],
            [3.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 3.5],
            [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5]
            ]
        rookValue = [
            [5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5],
            [5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [4.5, 5, 5, 5, 5, 5, 5, 4.5]
            ]
        queenValue = [
            [7.5, 8, 8, 8, 8, 8, 8, 7.5],
            [7.5, 8, 8, 8, 8, 8, 8, 7.5],
            [7.5, 8, 9, 9, 9, 9, 8, 7.5],
            [7.5, 8, 9, 9.2, 9.2, 9, 8, 7.5],
            [7.5, 8, 9, 9.2, 9.2, 9, 8, 7.5],
            [7.5, 8, 8, 8, 8, 8, 8, 7.5],
            [7.5, 8, 8, 8, 8, 8, 8, 7.5],
            [7.5, 8, 8, 8, 8, 8, 8, 7.5],
            ]
        kingValue = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1.2, 1.2, 1, 1, 1, 1.2, 1]
            ]

        piecesToValues = {"P": pawnValue, "N": knightValue, "B": bishopValue, "R": rookValue, "Q": queenValue, "K": kingValue}
        #piecesToValuess = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}

        eval = 0
        correction = 0
        for rowN, row in enumerate(gs.board):

            for pieceN, piece in enumerate(row):
                if piece[0] == "w":
                    eval += piecesToValues[piece[1]][rowN][pieceN]
                    #eval += piecesToValuess[piece[1]]


                elif piece[0] == "b":
                    eval -= piecesToValues[piece[1]][7 - rowN][7 - pieceN]
                    #eval -= piecesToValuess[piece[1]]

        if gs.inCheck(gs.whiteToMove):
            correction += 2
        if whitesMove:  # called in future moves
            eval += correction
            if gs.staleMate and eval > 0:
                eval -= 5
        else:
            eval -= correction
            if gs.staleMate and eval < 0:
                eval += 5

        return eval


    # engine makes a random move list out of all valid moves
    @classmethod
    def computerMoveRandom(cls, gs):

        moves = gs.getValidMoves(not gs.whiteToMove, True)

        move = random.choice(moves)
        gs.makeMove(move)

        return move

    # engine calculates the best possible board one move ahead
    @classmethod
    def computerMove(cls, gs):
        evals = []
        moves = gs.getValidMoves(not gs.whiteToMove, True)
        for move in moves:
            gs.makeMove(move)
            gs.getValidMoves(not gs.whiteToMove, True)
            evals.append(gs.evaluation(not gs.whiteToMove))
            gs.undoMove()
        if gs.whiteToMove:
            best = [i for i, x in enumerate(evals) if x == max(evals)]
        else:
            best = [i for i, x in enumerate(evals) if x == min(evals)]
        bestMoves = [moves[j] for j in best]
        move = random.choice(bestMoves)
        gs.makeMove(move)
        return move


    @classmethod
    def getEvaluation(cls, gs, move): # call with  pool.map(self.gs.getEvaluation, moves) for multithreading
        gs.makeMove(move)
        moves = gs.getValidMoves(not gs.whiteToMove, True)
        evals = [move.evaluation for move in moves]
        gs.undoMove()

        return evals


    @classmethod
    def miniMax(cls, gs, move): # call with  pool.map(self.gs.miniMax, moves) for multithreading

        gs.makeMove(move)
        eval1 = -1000  # maximizing
        moves = gs.getValidMoves(not gs.whiteToMove, True)
        if len(moves) > 0:
            for move in moves:
                gs.makeMove(move)
                moves2 = gs.getValidMoves(gs.whiteToMove, True)

                if len(moves2) > 0:
                    eval2 = 1000  # minimizing

                    for move2 in moves2:  
                        eval = move2.evaluation
                        if eval < eval2:
                            eval2 = eval

                if eval2 > eval1:
                    eval1 = eval2
                gs.undoMove()


            gs.undoMove()

        gs.undoMove()
        return eval1


    @classmethod
    def computerMoveProoo(cls, gs):  # 3 moves ahead
        start = time.time()

        moves = gs.getValidMoves(gs.whiteToMove, True)
        bestMoves = []
        pool = Pool(processes = len(moves), maxtasksperchild = 100)

        evals = pool.starmap(cls.miniMax, [(gs, move) for move in moves])
        evals += np.random.random(len(evals))*0.2  # non deterministic engine
        # print(evals)
        pool.terminate()

        best = np.argmin(evals)
        move = moves[best]
        gs.makeMove(move)
        stop = time.time()
        #print("nodes/s: ", round(self.gs.nodes / (stop-start), 2))
        #print("nodes: ", self.gs.nodes)

        return move


    @classmethod
    def notationTransform(cls, gs, moveIn, board=None, coordinateNotation=True):


        if coordinateNotation:  # easy notation already given

            moves = gs.getValidMoves(gs.whiteToMove, False)

            if moveIn == "O-O":
                return Move([7, 4], [7, 6], board)
            elif moveIn == "O-O-O":
                return Move([7, 4], [7, 2], board)

            filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
            colsToFiles = {i: j for j, i in filesToCols.items()}

            startSq = [8-int(moveIn[1]), filesToCols[moveIn[0]]]
            endSq = [8-int(moveIn[3]), filesToCols[moveIn[2]]]
            return Move(startSq, endSq, gs.board)

        else:

            moves = gs.getValidMoves(gs.whiteToMove, False)
            ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
            rowsToRanks = {i: j for j, i in ranksToRows.items()}

            filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
            colsToFiles = {i: j for j, i in filesToCols.items()}

            if moveIn == "O-O":
                return Move([7, 4], [7, 6], gs.board)
            elif moveIn == "O-O-O":
                return Move([7, 4], [7, 2], gs.board)

            moveIn = moveIn.replace("x", "")

            moveIn = moveIn.replace("+", "")
            moveIn = moveIn.replace("#", "")

            pieceMoved = moveIn[0]
            moveIn = moveIn[:-2] + str(ranksToRows[moveIn[-1]]) + str(filesToCols[moveIn[-2]])



            list = ["a", "b", "c", "d", "e", "f", "g", "h"]
            for c in list:
                if moveIn[0] == c:
                    moveIn = f"P{moveIn}"


            possibleMoves = [move for move in moves if str(move.endRow) == moveIn[-2] and str(move.endCol) == moveIn[-1]]

            if len(moveIn) == 2:
                moveIn = f"P{moveIn}"

            print(f"{possibleMoves=}")
            finalMoves = [move for move in possibleMoves if moveIn[0] == move.pieceMoved[1]]

            print(f"{finalMoves=}")

            if len(finalMoves) > 1:
                print("multiple moves available")
                for move in finalMoves:
                            

                    if moveIn[1] not in [colsToFiles[move.startCol], rowsToRanks[move.startRow]]:
                        finalMoves.remove(move)
                        print(f"removed: {move.getChessNotation()}")
            if len(finalMoves) > 1:
                print("error")
            return(finalMoves[0])


