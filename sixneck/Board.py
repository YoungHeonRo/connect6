import numpy as np

class Board:
    def __init__(self, size):
        self.size = size
        self.state = [[0 for i in range(size)] for j in range(size)]
        self.available_moves = [[x, y] for x in range(size) for y in range(size)]
        self.prev_moves = [[size//2, size//2], [size//2, size//2]]
        self.prev_mine = [ [-1,-1], [-1,-1] ]
        self.threat = [[0 for i in range(size)] for j in range(size)]
        self.threat_offense = [[0 for i in range(size)] for j in range(size)]
        self.count = 0
        self.threat_chosen = []
        self.final_move = []
        self.best_moves = []
        self.active_area = []

    def player_in_turn(self):
        return 1 if self.count % 4 in [0, 3] else 2

    def get_last_move(self):
        return self.prev_moves[1-self.count%2]

    # input: x, y
    def update(self, move):
        x, y = move

        self.prev_mine[self.count%2] = self.prev_moves[self.count%2]
        self.prev_moves[self.count%2] = [x,y]

        self.state[x][y] = self.player_in_turn()
        self.available_moves.remove(move)
        self.update_active_area(move)

        self.count += 1

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

    def evaluate(self, board, half_move):
        s_index = board.s_index

        size = board.size
        state = board.state
        x, y = half_move

        e = math.exp(1)
        #player_weight = [0.0, 1.0, 2.0, 6.0, 0.0, 0.0, 0.0]
        #opponent_weight = [0.0, -1.05, -5.0, -11.05, 0.0, 0.0, 0.0]
        player_weight = [0.0, e**2, e**3, e**6, e**6, e**30, 0.0]
        opponent_weight = [-0.0, -e**2, -e**4, -e**10, -e**10, -e**29, -0.0]

        for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
            for i in range(6): #right to left
                if x+dx*(-i) >= 0 and x+dx*(-i+5) < size and y+dy*(-i) >= 0 and y+dy*(-i+5) < size and y+dy*(-i) < size and y+dy*(-i+5) >= 0:
                    index = list([x+dx*(-i+j), y+dy*(-i+j)] for j in range(6))
                    index = index[::-1]
                    window = list(state[x][y] for x, y in index)
                    if self.opponent not in window:
                        cnt = window.count(self.player)
                        if board.player_in_turn() == self.player:
                            s_index += player_weight[cnt]
                        s_index -= player_weight[cnt-1]
                    elif self.player not in window:
                        cnt = window.count(self.opponent)
                        if board.player_in_turn() == self.opponent:
                            s_index += opponent_weight[cnt]
                        s_index -= opponent_weight[cnt-1]

        return s_index
