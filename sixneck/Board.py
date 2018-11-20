import numpy as np

class Board:
    def __init__(self, size):
        self.size = size
        self.state = np.zeros((size, size), dtype=int)
        self.available_moves = [[x, y] for x in range(size) for y in range(size)]
        self.prev_moves = [[size//2, size//2], [size//2, size//2]]
        self.prev_mine = [ [-1,-1], [-1,-1] ]
        self.threat = [[0 for i in range(size)] for j in range(size)]
        self.threat_offense = [[0 for i in range(size)] for j in range(size)]
        self.count = 0
        self.threat_chosen = []
        self.final_move = []
        self.active_area = []
        self.s_index = 0

    def player_in_turn(self):
        return 1 if self.count % 4 in [0, 3] else 2

    def get_last_move(self):
        return self.prev_moves[1-self.count%2]

    def update_active_area(self, half_move, distance=2):
        size = self.size
        state = self.state
        x, y = half_move
        for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
            for l in [-1, 1]:
                for k in range(1, distance+1):
                    tx = x+dx*l*k
                    ty = y+dy*l*k
                    if [tx, ty] in self.available_moves and [tx, ty] not in self.active_area:
                        self.active_area.append([tx, ty])
        if half_move in self.active_area:
            self.active_area.remove(half_move)

    # input: x, y
    def update(self, move):
        x, y = move
        self.state[x][y] = self.player_in_turn()
        self.available_moves.remove(move)
        self.prev_mine[self.count%2] = self.prev_moves[self.count%2]
        self.prev_moves[self.count%2] = [x,y]
        self.update_active_area(move)
        self.count += 1

    # output: winner(0: draw, 1: black wins, 2: white wins, -1: no winner yet)
    def get_winner(self):
        size = self.size
        state = self.state
        x, y = self.get_last_move()
        winner = state[x][y]

        for i in range(6):
            if x-i >= 0 and x-i+5 < size:
                if len(set(state[x-i+j][y] for j in range(6))) == 1:
                    return winner

            if y-i >= 0 and y-i+5 < size:
                if len(set(state[x][y-i+j] for j in range(6))) == 1:
                    return winner

            if x-i >= 0 and x-i+5 < size and y-i >= 0 and y-i+5 < size:
                if len(set(state[x-i+j][y-i+j] for j in range(6))) == 1:
                    return winner

            if x-i >= 0 and x-i+5 < size and y+i-5 >= 0 and y+i < size:
                if len(set(state[x-i+j][y+i-j] for j in range(6))) == 1:
                    return winner

        if self.count >= size * size:
            return 0

        return -1
