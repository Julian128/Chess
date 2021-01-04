from multiprocessing import Process, Queue, Pool
import lichess.api
from lichess.format import SINGLE_PGN
import time
import os
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


def main():
    #token = "lMysRaNxd9sNQkXj"  rodfish
    token = "b0X9NKGbCQ3XWpz3"  # coffebot
    session = berserk.TokenSession(token)
    client = berserk.Client(session)
    #client.account.upgrade_to_bot()
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

            state = client.games.export(game_id)
            moves = state["moves"]

            move = moves.split()
            
            if len(move) % 2 == 1:

                moveE = gs.notationTransform(move[-1])  # enemy move
                print(moveE.getChessNotation())
                move = gs.makeMove(moveE)
                movecount += 1

                moveMade = True
                if moveMade:
                    validMoves = gs.getValidMoves(gs.whiteToMove, False)  # detects checkmate, stalemate
                    if gs.checkMate:
                        client.bots.post_message(game_id, "gg")
                        print("MATE")
                    moveMade = False
            else:
                time.sleep(0.5)

        if(not gs.whiteToMove):  # bot playing a move

            validMoves = gs.getValidMoves(gs.whiteToMove, False)
            if len(validMoves) > 0:

                move = gs.computerMoveProoo()
                print(str(move.getChessNotation()))            
                client.bots.make_move(game_id, str(move.getChessNotation()))

                print("evaluation: ", round(gs.evaluation(gs.whiteToMove), 2))
                moveMade = True
                if moveMade:
                    validMoves = gs.getValidMoves(gs.whiteToMove, False)  # detects checkmate, stalemate
                    if gs.checkMate:
                        client.bots.post_message(game_id, "gg")
                        print("MATE")
                    moveMade = False




if __name__ == "__main__":
    main()