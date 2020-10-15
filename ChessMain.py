

import pygame as pyg
import ChessEngine


width = height = 1024
dimensions = 8
sq_size = height / dimensions
maxFPS = 60
images = {}  # initializes a set, an unordered colletion with no dupilcate elements


#Initialize global dict of images, called once

def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (int(sq_size), int(sq_size)))


def main():
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
            elif i.type == pyg.KEYDOWN:
                if i.key == pyg.K_LEFT:
                    gs.undoMove()
                    moveMade = True
                    print("undo")
                    print("undo")
                if i.key == pyg.K_RIGHT:
                    gs.redoMove()
                    print("redo")

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
                    print(move.getChessNotation())

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:  # fixes double click bug
                        playerClicks = [sqSelected]

    

        if moveMade:
            validMoves = gs.getValidMoves()
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