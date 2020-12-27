from multiprocessing import Process, Queue, Pool
import lichess.api
from lichess.format import SINGLE_PGN
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg
import ChessEngine
import random



width = height = 1024
dimensions = 8
sq_size = height / dimensions
maxFPS = 60
images = {}  # initializes a set, an unordered collection with no dupilcate elements


#Initialize global dict of images, called once

def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (int(sq_size), int(sq_size)))


def main():

    #user = lichess.api.user('Julik137')
    #print(user['perfs']['blitz']['rating'])
    #pgn = lichess.api.user_games('Julik137', max=1, format=SINGLE_PGN)
    #pgn = lichess.api.game('Qa7FJNk2', format=PGN)
    #print(pgn)


    pyg.init()
    screen = pyg.display.set_mode((width, height))
    clock = pyg.time.Clock()
    screen.fill(pyg.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made

    loadImages()

    running = True

    sqSelected = ()  # tuple keeping track of last square clicked
    playerClicks = []  # track two mouse clicks

    while running:
        for i in pyg.event.get():
            if i.type == pyg.QUIT:  # keyboard clicks
                running = False

            #play against engine
            if not gs.whiteToMove:
                if len(validMoves) > 0:

                    start = time.time()
                    #gs.nodes = 0
                    move = gs.computerMovePro()
                    print(round(gs.evaluation(gs.whiteToMove), 2))

                    print(move.getChessNotation())
                    done = time.time()
                    #print("nodes/s: " + str(round((gs.nodes / (done - start)))))

                    moveMade = True
                    if moveMade:
                        validMoves = gs.getValidMoves()  # detects checkmate, stalemate
                        if gs.checkMate:
                            print("MATE")
                        moveMade = False


            elif i.type == pyg.KEYDOWN:
                if i.key == pyg.K_LEFT:
                    gs.undoMove()
                    moveMade = True
                    print("undo")
                #if i.key == pyg.K_RIGHT:
                    #gs.redoMove()
                    #print("redo")


                # COMPUTER MOVES
                if i.key == pyg.K_e:
                    for i in range(0, 100):
                        if len(validMoves) > 0:

                            gs.nodes = 0
                            start = time.time()

                            if gs.whiteToMove:
                                move = gs.computerMovePro()
                            else:
                                move = gs.computerMove()

                            print(move.getChessNotation())
                            done = time.time()

                            print("nodes: " + str(gs.nodes))#str(round((gs.nodes / (done - start)))))

                            moveMade = True
                            #print(gs.evaluation())
                                




                            drawGameState(screen, gs)
                            clock.tick(maxFPS)
                            pyg.display.flip()



            elif i.type == pyg.MOUSEBUTTONDOWN:  # mouse clicks
                location = pyg.mouse.get_pos()  # x, y location of mouse
                col = int(location[0] // sq_size)
                row = int(location[1] // sq_size)
                if sqSelected == (row, col):
                    sqSelected == ()  # unselect square
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                    if move in validMoves:

                        print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:  # fixes double click bug
                        playerClicks = [sqSelected]


    
                            
        if moveMade:
            validMoves = gs.getValidMoves()  # detects checkmate, stalemate
            if gs.checkMate:
                print("MATE")
            moveMade = False



        drawGameState(screen, gs)
        clock.tick(maxFPS)
        pyg.display.flip()



def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [pyg.Color("gray"), pyg.Color("dark green")]

    for i in range(dimensions):  # rows
        for j in range(dimensions):  # columns
            color = colors[((i + j) % 2)]
            pyg.draw.rect(screen, color, pyg.Rect(j * sq_size, i * sq_size, sq_size, sq_size))


def drawPieces(screen, board):
    for i in range(dimensions):
        for j in range(dimensions):
            piece = board[i][j]

            if piece != "--":  # not empty square
                screen.blit(images[piece], pyg.Rect(j * sq_size, i * sq_size, sq_size, sq_size))




if __name__ == "__main__":
    main()