class Board:
    def __init__(self, size):
        self.size = size
        self.state = [[0 for i in range(size)] for j in range(size)]
        self.threat = [[0 for i in range(size)] for j in range(size)]
        self.count = 0
        self.prev = []

    def player_in_turn(self):
        return 1 if self.count % 4 in [0, 3] else 2
    
    # update the move and print the board
    # (input: x, y of the move and player's color / output: winner)
    def update(self, x, y):
        #color = 'black' if self.player_in_turn() == 1 else 'white'
        #print(color + ':', str(x), str(y))
        self.prev = (x,y)
        self.state[x][y] = self.player_in_turn()
        winner = self.check(x, y)

        self.count += 1

        return winner

    #def getMove(self):

    
    # check if the game is end (input: (x, y) of the last move / output: winner)
    # <winner> 0: draw, 1: black wins, 2: white wins, -1: no winner yet
    def check(self, x, y):
        size = self.size
        winner = self.player_in_turn()
        
        for i in range(6):
            if x-i >= 0 and x-i+5 < size:
                if len(set(self.state[x-i+j][y] for j in range(6))) == 1:
                    return winner
                
            if y-i >= 0 and y-i+5 < size:
                if len(set(self.state[x][y-i+j] for j in range(6))) == 1:
                    return winner
                
            if x-i >= 0 and x-i+5 < size and y-i >= 0 and y-i+5 < size:
                if len(set(self.state[x-i+j][y-i+j] for j in range(6))) == 1:
                    return winner

            if x-i >= 0 and x-i+5 < size and y+i-5 >= 0 and y+i < size:
                if len(set(self.state[x-i+j][y+i-j] for j in range(6))) == 1:
                    return winner

        if self.count >= self.size * self.size:
            return 0

        return -1

    
