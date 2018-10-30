from HalfMove import *

class Player():
    
    def __init__(self, color):
        self.color = color

class rule_based_AI():

    def __init__(self, color):
        self.color = color

    def threatMove(self, board, prev_moves):
        threat = [[0 for i in range(board.size)] for j in range(board.size)]

        for x, y in prev_moves:
            #x-axis
            for i in range(0, 6):
                stones_in_window = 0
                empty_idx = []
                if x-i < 0:
                    break
                elif x+5-i >= board.size:
                    continue
                for j in range(0, 6):
                    if board.state[x-i+j][y] == 3-self.color:
                        stones_in_window+=1
                    elif board.state[x-i+j][y] == 0:
                        empty_idx.append( (x-i+j,y) )
                    else :
                        empty_idx.clear()
                        break
                if stones_in_window >=4 :
                    for x,y in empty_idx:
                        board.threat[x][y] += 1
            #y-axis
            for i in range(0, 6):
                stones_in_window = 0
                empty_idx = []
                if y-i < 0:
                    break
                elif y+5-i >= board.size:
                    continue
                for j in range(0, 6):
                    if board.state[x][y-i+j] == 3-self.color:
                        stones_in_window+=1
                    elif board.state[x][y-i+j] == 0:
                        empty_idx.append( (x,y-i+j) )
                    else :
                        empty_idx.clear()
                        break
                if stones_in_window >=4 :
                    for x,y in empty_idx:
                        board.threat[x][y] += 1
            #diagonal axis(1)
            for i in range(0, 6):
                stones_in_window = 0
                empty_idx = []
                if x-i <0 or y-i < 0:
                    break
                elif x+5-i >= board.size or y+5-i >= board.size:
                    continue
                for j in range(0, 6):
                    if board.state[x-i+j][y-i+j] == 3-self.color:
                        stones_in_window+=1
                    elif board.state[x-i+j][y-i+j] == 0:
                        empty_idx.append( (x-i+j,y-i+j) )
                    else :
                        empty_idx.clear()
                        break
                if stones_in_window >=4 :
                    for x,y in empty_idx:
                        board.threat[x][y] += 1
            #diagonal axis(2)
            for i in range(0, 6):
                stones_in_window = 0
                empty_idx = []
                if x-i <0 or y+i >= board.size:
                    break
                elif x+5-i >= board.size or y-5+i < 0:
                    continue
                for j in range(0, 6):
                    if board.state[x-i+j][y+i-j] == 3-self.color:
                        stones_in_window+=1
                    elif board.state[x-i+j][y+i-j] == 0:
                        empty_idx.append( (x-i+j,y+i-j) )
                    else :
                        empty_idx.clear()
                        break
                if stones_in_window >=4 :
                    for x,y in empty_idx:
                        board.threat[x][y] += 1

        max_threat=0
        defensive_moves = []
        #make a list of moves with max_threat(>=2)
        for i in range(board.size):
            for j in range(board.size):
                if threat[i][j] > max_threat:
                    defensive_moves.clear()
                    defensive_moves.append([i,j])
                    max_threat = threat[i][j]
                elif threat[i][j] == max_threat:
                    defensive_moves.append([i,j])

        if max_threat < 2 :
            self.defensive_moves = []
            return []
        else :
            self.defensive_moves = defensive_moves
            return defensive_moves

    def get_move(self, board, defensive_moves):
        if len(defensive_moves)==1 :
            i, j = defensive_moves
            defensive_moves.clear()
            return i,j
        else :
            #do halfMove within defensive_moves
            max_score=0
            for i in range(0,19):
                for j in range(0,19):
                    if board.state[i][j] != 0: continue
                    if len(defensive_moves) > 1 and [i, j] not in defensive_moves:
                        continue
                    temp1 = halfMove(board, i, j, self.color)
                    #temp2 = halfMove(board, i, j, 3 - self.color)
                    #print(temp,end=' ')
                    if temp1 >= max_score :
                        max_score = temp1
                        max_i = i
                        max_j = j
                    #print('(',i,',',j,')',temp1, end=' ')
                #print()

            return max_i, max_j
            

    def my_sort(self, x):
        return x[-1]

            

        
def init_player(color, option):
    if option == 'rb':
        return rule_based_AI(color)
    return Player(color)
