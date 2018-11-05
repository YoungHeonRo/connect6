class Board:
    def __init__(self, size):
        self.size = size
        self.state = [[0 for i in range(size)] for j in range(size)]
        self.available_moves = [[x, y] for x in range(size) for y in range(size)]
        self.prev_moves = [[size//2, size//2], [size//2, size//2]]
        self.count = 0
        self.threat = [[0 for i in range(size)] for j in range(size)]


    def player_in_turn(self):
        return 1 if self.count % 4 in [0, 3] else 2

    def get_last_move(self):
        return self.prev_moves[1-self.count%2]

    # input: x, y
    def update(self, x, y):
        self.state[x][y] = self.player_in_turn()
        self.available_moves.remove([x,y])
        self.prev_moves[self.count%2] = [x,y]
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
