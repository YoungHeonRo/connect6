import tkinter as tk

from Board import *

size = 19
canvas_size = size*30 + 30

class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.human = 1
        self.init_board()
        self.init_widgets()

    def init_board(self):
        self.canvas = tk.Canvas(self, height=canvas_size, width=canvas_size, background='#c98003')
        for x in range(size):
            self.canvas.create_line(30 + x*30, 30, 30 + x*30, canvas_size-30) 
        for y in range(size):
            self.canvas.create_line(30, 30 + y*30, canvas_size-30, 30 + y*30)
        r = 2
        for x in range(3, size, 6):
            for y in range(3, size, 6):
                self.canvas.create_oval(30 + x*30-r, 30 + y*30-r, 30 + x*30+r, 30 + y*30+r, fill='black')

        self.board = Board(size)
        if self.human == 2:
            self.doMove(size//2, size//2)
        self.canvas.bind('<Button-1>', self.getXY)
        self.canvas.pack()

    def init_widgets(self):
        self.reset = tk.Button(self, text='reset', command=self.resetBoard)
        self.reset.pack(side='bottom')
        self.last_move = tk.Label(self, text='Hello World')
        self.last_move.pack(side='bottom')

    def resetBoard(self):
        self.canvas.destroy()
        self.human = 3 - self.human
        self.init_board()
        self.last_move['text'] = 'Hello World'
    
    def getXY(self, event):
        x = round(event.x/30 - 1)
        y = round(event.y/30 - 1)
        self.doMove(x, y)
        
    def doMove(self, x, y):
        board = self.board
        
        if x < 0 or x>= size or y < 0 or y >= size or board.state[x][y] != 0:
            #print('invalid move')
            #self.last_move['text'] = 'invalid move'
            return
        
        else:
            r = 10
            color = 'black' if board.player_in_turn() == 1 else 'white'
            self.canvas.create_oval(30 + x*30-r, 30 + y*30-r, 30 + x*30+r, 30 + y*30+r, fill=color)

            winner = board.update(x, y)
            if self.last_move['text'][:5] == color:
                self.last_move['text'] += ' / x: ' + str(x) + ', y: ' + str(y)
            else:
                self.last_move['text'] = color + ' x: ' + str(x) + ', y: ' + str(y)
            if winner >= 0:
                #print(['draw', 'black won', 'white won'][winner])
                self.last_move['text'] = ['draw', 'black won', 'white won'][winner]
                self.canvas.unbind('<Button-1>')

        if board.player_in_turn() != self.human:
            #x, y = AI_move(board)
            #self.doMove(x, y)
            pass
        
root = tk.Tk()
game = Game(root)
game.mainloop()

