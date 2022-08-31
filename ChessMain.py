"""
Interacts through berserk with the lichess API to play online against any Lichess player upon invitation.
"""


import time
import src.GameState as GameState
from src.GameState import Move
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
    token = "b0X9NKGbCQ3XWpz3"  # coffeebot
    session = berserk.TokenSession(token)
    client = berserk.Client(session)
    #client.account.upgrade_to_bot()
    in_game = False
    numberOfMoves = 0    

    while(not in_game):
        "Waiting for challenge.."
        time.sleep(2)
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




    gs = GameState.GameState()
    moveMade = False  # flag variable for when a move is made
    numberOfMoves = 1
    while in_game:

        g = Game(client, game_id)
        moveList = g.current_state["state"]["moves"]

        moves = moveList.split()
        print(moves)

        if len(moves) < numberOfMoves or moveList[0] == "":
            time.sleep(1)
            continue

        numberOfMoves == len(moveList)

        # print(gs.board)


        if gs.whiteToMove:  # importing enemy move


            if len(moves) % 2 == 1:
            # if True:
                moveE = gs.notationTransform(str(moves[-1]), gs.board)  # enemy move

                # moveE = Move(move[-1][:2], move[-1][2:], gs.board)  # enemy move

                print(moveE.getChessNotation())
                move = gs.makeMove(moveE)
                print(gs.board)
                print("white move made")

                if moveMade := True:
                    validMoves = gs.getValidMoves(gs.whiteToMove, False)  # detects checkmate, stalemate
                    if gs.checkMate:
                        client.bots.post_message(game_id, "gg Easy")
                        print("MATE")
                    moveMade = False
            else:
                time.sleep(0.5)


        if (not gs.whiteToMove):  # bot playing a move

            validMoves = gs.getValidMoves(gs.whiteToMove, False)
            if len(validMoves) > 0:

                # move = gs.computerMoveRandom()
                move = gs.computerMoveProoo()
                print(str(move.getChessNotation()))
                client.bots.make_move(game_id, str(move.getChessNotation()))

                print("evaluation: ", round(gs.evaluation(gs.whiteToMove), 2))
                if moveMade := True:
                    validMoves = gs.getValidMoves(gs.whiteToMove, False)  # detects checkmate, stalemate
                    if gs.checkMate:
                        client.bots.post_message(game_id, "gg")
                        print("MATE")
                    moveMade = False


        time.sleep(0.5)

if __name__ == "__main__":
    main()