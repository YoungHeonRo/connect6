import time
import math
import copy

from Board import *
from AI import Bot

size = 19

class Game():
    def __init__(self, depth1, beam1, depth2, beam2, master=None):
        self.human = 1
        self.depth1 = depth1
        self.depth2 = depth2
        self.beam1 = beam1
        self.beam2 = beam2
        self.second = 0
        self.AI = Bot(3 - self.human, depth=self.depth1, beam_size=self.beam1)
        self.AI2 = Bot(self.human, depth=self.depth2, beam_size=self.beam2)
        self.self_play = True
        self.init_board()

    def init_board(self):
        self.board = Board(size)
        if self.human == 2 or self.self_play == True:
            self.doMove([size//2, size//2])

    def resetBoard(self):
        self.canvas.destroy()
        self.AI = Bot(self.human)
        self.AI2 = Bot(3 - self.human, beam_size=2)
        self.human = 3 - self.human
        self.init_board()

    def getXY(self, event):
        x = round(event.x/30 - 1)
        y = round(event.y/30 - 1)
        self.doMove([x, y])

    def doMove(self, move):
        board = self.board
        x, y = move
        if x < 0 or x>= size or y < 0 or y >= size or board.state[x][y] != 0:
            return

        else:
            r = 10
            color = 'black' if board.player_in_turn() == 1 else 'white'

            board.update(move)

            #print(color, 'x:', x, 'y:', y)
            win_color = board.get_winner(move)
            if win_color >= 0:
                win = 'black' if win_color == 1 else 'white'
                print("winner : " + win )
                return

        if board.player_in_turn() == self.AI.player:
            #print('AI:', end=' ')
            move = self.AI.predict(board)
            self.doMove(move)
        elif self.self_play == True and board.player_in_turn() == self.AI2.player:
            #print('AI2:', end=' ')
            move = self.AI2.predict(board)
            self.doMove(move)

    

if __name__ == "__main__":

    for depth1 in range(3, 6):
        for depth2 in range(3, 6):
            for beam1 in range(1,6):
                for beam2 in range(1,6):
                    if depth1 < depth2 and beam1 < beam2 :
                        print(str(depth1) +" "+ str(beam1), end=' vs ')
                        print(str(depth2) +" "+ str(beam2))
                        gg = Game(depth1, beam1, depth2, beam2)
                        if( (beam1 == beam2) and (depth1 == depth2) ) :
                            continue
                        print(str(depth2) +" "+ str(beam2), end=' vs ')
                        print(str(depth1) +" "+ str(beam1))
                        gg = Game(depth2, beam1, depth2, beam1)

