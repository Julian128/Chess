from multiprocessing import Process, Queue, Pool
import lichess.api
from lichess.format import SINGLE_PGN
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg
import ChessEngine
import random
import berserk
import threading



class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)

    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    def handle_state_change(self, game_state):
        pass

    def handle_chat_line(self, chat_line):
        pass


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
    token = "lMysRaNxd9sNQkXj"
    session = berserk.TokenSession(token)
    client = berserk.Client(session)

    in_game = False
    while(not in_game):

        time.sleep(0.5)
        for event in client.bots.stream_incoming_events():
            if event['type'] == 'gameStart':
                game_id = event['game']['id']
                in_game = True
                break
            elif event['type'] == 'challenge':
                game_id = event['challenge']['id']
                client.bots.accept_challenge(game_id)
                client.bots.post_message(game_id, "glhf")
                in_game = True
    print("The game has started!")

    gs = ChessEngine.GameState()
    moveMade = False  # flag variable for when a move is made
    while(in_game):
        movecount = 0
        state = client.games.export(game_id)
        move = state["moves"]

        if(gs.whiteToMove):  # importing enemy move



            move = ""
            last_move = ""

            state = client.games.export(game_id)
            moves = state["moves"]

            move = moves.split()
            time.sleep(1)
            
            if len(move) % 2 == 1:
                start = time.time()

                #gs.nodes = 0
                #print(move[-1])
                
                moveE = gs.notationTransform(move[-1])  # enemy move
                print(moveE.getChessNotation())
                move = gs.makeMove(moveE)
                #for i in range(0, len(gs.board)):
                    ##print(str(gs.board[i]) + "\n")
                movecount += 1
                done = time.time()
                #print("nodes/s: " + str(round((gs.nodes / (done - start)))))

                moveMade = True
                if moveMade:
                    validMoves = gs.getValidMoves(gs.whiteToMove)  # detects checkmate, stalemate
                    if gs.checkMate:
                        client.bots.post_message(game_id, "gg")
                        print("MATE")
                    moveMade = False


        if(not gs.whiteToMove):  # bot playing a move

            validMoves = gs.getValidMoves(gs.whiteToMove)
            if len(validMoves) > 0:

                start = time.time()
                #gs.nodes = 0
                move = gs.computerMovePro()
                print(str(move.getChessNotation()))
            
                client.bots.make_move(game_id, str(move.getChessNotation()))
                #for i in range(0, len(gs.board)):
                #    print(str(gs.board[i]) + "\n")
                done = time.time()
                #print("nodes/s: " + str(round((gs.nodes / (done - start)))))
                print(round(gs.evaluation(gs.whiteToMove), 2))
                moveMade = True
                if moveMade:
                    validMoves = gs.getValidMoves(gs.whiteToMove)  # detects checkmate, stalemate
                    if gs.checkMate:
                        print("MATE")
                    moveMade = False




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
                    print(move.getChessNotation())
                    done = time.time()
                    print("nodes/s: " + str(round((gs.nodes / (done - start)))))

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