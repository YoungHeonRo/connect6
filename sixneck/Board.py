class Board:
    def __init__(self, size):
        self.size = size
        self.state = [[0 for i in range(size)] for j in range(size)]
        self.available_moves = [[x, y] for x in range(size) for y in range(size)]
        self.active_area = []
        self.count = 0
        self.winner = -1

    def player_in_turn(self):
        return 1 if self.count % 4 in [0, 3] else 2

    def update(self, move):
        x, y = move

        self.state[x][y] = self.player_in_turn()
        self.available_moves.remove(move)
        self.active_area = self.find_active_area(move)

        self.count += 1

    def find_active_area(self, half_move, distance=2):
        active_area = self.active_area

        size = self.size
        state = self.state
        x, y = half_move
        for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
            for l in [-1, 1]:
                for k in range(1, distance+1):
                    tx = x+dx*l*k
                    ty = y+dy*l*k
                    if [tx, ty] in self.available_moves and [tx, ty] not in active_area:
                        active_area.append([tx, ty])
        if half_move in active_area:
            active_area.remove(half_move)

        return active_area

    # output: winner(0: draw, 1: black wins, 2: white wins, -1: no winner yet)
    def get_winner(self, move):
        x, y = move
        size = self.size
        state = self.state
        self.winner = state[x][y]

        for i in range(6):
            if x-i >= 0 and x-i+5 < size:
                if len(set(state[x-i+j][y] for j in range(6))) == 1:
                    return self.winner
            if y-i >= 0 and y-i+5 < size:
                if len(set(state[x][y-i+j] for j in range(6))) == 1:
                    return self.winner
            if x-i >= 0 and x-i+5 < size and y-i >= 0 and y-i+5 < size:
                if len(set(state[x-i+j][y-i+j] for j in range(6))) == 1:
                    return self.winner
            if x-i >= 0 and x-i+5 < size and y+i-5 >= 0 and y+i < size:
                if len(set(state[x-i+j][y+i-j] for j in range(6))) == 1:
                    return self.winner

        if self.count >= size * size:
            return 0

        return -1
