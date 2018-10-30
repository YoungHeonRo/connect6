class Board:
    
    # need documentation
    def __init__(self, size):
        self.size=19
        self.state = [[0 for i in range(size)] for j in range(size)]
        self.count = 0
        #self.white_priority = [[0 for i in range(size)] for j in range(size)]
        self.threat = [[0 for i in range(size)] for j in range(size)]
        self.color = 1
    def print(self):
        symbol = ['.', 'o', 'x']

        line = '\n '
        for i in range(self.size):
            line = line + format(i, '3d') + ' '
        print(line + ' x')
        
        for i in range(self.size):
            line = format(i, '2d') + ' '
            for j in range(self.size):
                line += symbol[self.state[i][j]] + '   '
            print(line + '\n')
        print('y\n')
    
    # update the move and print the board
    # (input: x, y of the move and player's color / output: is_end, winner)
    def update(self, x, y):
        self.state[x][y] = color
        self.count += 1
        self.print()
        return self.check(x, y)

    def changeColor(self):
        self.color = 3 - self.color
    
    # check if the game is end (input: x, y of the last move / output: is_end, winner)
    def check(self, x, y):
        #should be changed
        size=self.size
        for i in range(6):
            if x+i-5 >= 0 and x+i < size and len(set(self.state[x+j][y] for j in range(i-5, i+1))) == 1:
                return True, self.state[x][y]
        
        for i in range(6):
            if y+i-5 >= 0 and y+i < size and len(set(self.state[x][y+j] for j in range(i-5, i+1))) == 1:
                return True, self.state[x][y]
       
        for i in range(6):
            if x+i-5 >= 0 and x+i < size and y+i-5 >=0 and y+i < size and len(set(self.state[x+j][y+j] for j in range(i-5, i+1))) == 1:
                return True, self.state[x][y]

        for i in range(6):
            if x+i-5 >= 0 and x+i < size and y-i+5 < size and y-i >= 0 and len(set(self.state[x+j][y-j] for j in range(i-5, i+1))) == 1:
                return True, self.state[x][y]
            
        if self.count >= self.size * self.size:
            return True, -1

        return False, -1

    def clone(self):
        gb = gameBoard()
   
