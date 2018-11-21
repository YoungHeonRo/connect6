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
        self.AI_white = Bot(3 - self.human, depth=self.depth1, beam_size=self.beam1)
        self.AI_black = Bot(self.human, depth=self.depth2, beam_size=self.beam2)
        self.self_play = True
        self.init_board()

    def init_board(self):
        self.board = Board(size)
        if self.human == 2 or self.self_play == True:
            self.doMove([size//2, size//2])

    def resetBoard(self):
        self.canvas.destroy()
        self.AI_white = Bot(self.human)
        self.AI_black = Bot(3 - self.human)
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
                print(win + " win")
                return win

        if board.player_in_turn() == self.AI_white.player:
            #print('AI_white:', end=' ')
            move = self.AI_white.predict(board)
            self.doMove(move)
        elif self.self_play == True and board.player_in_turn() == self.AI_black.player:
            #print('AI_black:', end=' ')
            move = self.AI_black.predict(board)
            self.doMove(move)

    

if __name__ == "__main__":

    for depth1 in range(3, 6):
        for depth2 in range(3, 6):
            if depth1 <= depth2:
                for beam1 in range(1,5):
                    for beam2 in range(1,5):
                        if beam1 <= beam2 :
                            print('\n')
                            print(str(depth1) +" "+ str(beam1), end=' vs ')
                            print(str(depth2) +" "+ str(beam2), end=' : ')
                            gg = Game(depth2, beam2, depth1, beam1)
                            if( (beam1 == beam2) and (depth1 == depth2) ) :
                                continue
                            print(str(depth2) +" "+ str(beam2), end=' vs ')
                            print(str(depth1) +" "+ str(beam1), end=' : ')
                            gg = Game(depth1, beam1, depth2, beam2)

