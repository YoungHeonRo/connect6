import copy
import math

class Bot:
    def __init__(self, color):
        self.player = color
        self.opponent = 3 - color

    def beam_search(self, board, depth=2, beam_size=1):
        size = board.size
        best_moves = []

        for half_move1 in board.active_area:
            b = copy.deepcopy(board)
            b.update(half_move1)
            for half_move2 in b.active_area:
                x1, y1 = half_move1
                x2, y2 = half_move2
                if x1*size+y1 < x2*size+y2:
                    score = self.evaluate(board, half_move1) + self.evaluate(b, half_move2)
                    best_moves.append([half_move1, half_move2, score])

        best_moves.sort(key=lambda a:a[-1], reverse=(board.player_in_turn() == self.player))
        best_moves = best_moves[:beam_size]

        if depth > 1:
            children = []
            for moves in best_moves:
                b = copy.deepcopy(board)
                b.update(moves[0])
                b.update(moves[1])
                child = self.beam_search(b, depth-1, beam_size)
                children.append([moves[0], moves[1], child[-1]+moves[-1]])
            return max(children, key=lambda a:a[-1])
        else:
            return best_moves[0]

    def evaluate(self, board, half_move):
        s_index = 0

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

    def findFinalMoves(self, board):
        offensive_threat = self.threatSearch(board, 1)
        if offensive_threat > 0:
            offensive_moves = []
            for i in range(board.size):
                for j in range(board.size):
                    if [i, j] in board.available_moves and board.threat_offense[i][j] >= 2:
                        offensive_moves.append( [i, j] )

            for first_i, first_j in offensive_moves:
                for second_i, second_j in offensive_moves:
                    if (first_i*board.size+first_j) > (second_i*board.size+second_j) :
                        b=copy.deepcopy(board)
                        b.update([first_i, first_j])
                        b.update([second_i, second_j])
                        if b.get_winner() > 0 :
                            board.final_move = [ [first_i, first_j], [second_i, second_j] ]

    def findDefensiveMoves(self, board):
        size = board.size
        state = board.state

        threat_len = self.threatSearch(board)
        #print('threat_len :', threat_len)

        defensive_moves = []
        for i in range(size):
            for j in range(size):
                if [i, j] in board.available_moves and board.threat[i][j] >= 2:
                    defensive_moves.append([i, j, board.threat[i][j]])

        defensive_moves.sort(key=lambda a:a[-1], reverse=True)
        defensive_moves = [[i,j] for i,j,k in defensive_moves]

        board.threat_chosen=[]
        #print('defensive_moves :', defensive_moves)

        threat_candidate = []
        if threat_len == 1:
            #move = defensive_moves[0]
            for one_i, one_j in defensive_moves:
                temp_board = copy.deepcopy(board)
                temp_board.state[one_i][one_j] = temp_board.player_in_turn()
                temp_threat_len = self.threatSearch(temp_board)
                if temp_threat_len == 0:
                    threat_candidate.append( [one_i, one_j] )

            if len(threat_candidate) >= 1:
                board.threat_chosen.append( threat_candidate[0] )

        elif threat_len >= 2:
            #defensive moves : i, j, threat value
            for first_i, first_j in defensive_moves :
                for second_i, second_j in defensive_moves :
                    if (first_i*board.size+first_j) > (second_i*board.size+second_j) :
                        temp_board = copy.deepcopy(board)
                        temp_board.state[first_i][first_j] = temp_board.player_in_turn()
                        temp_board.state[second_i][second_j] = temp_board.player_in_turn()
                        temp_threat_len = self.threatSearch(temp_board)
                        if temp_threat_len == 0 and [ [second_i, second_j] , [first_i,first_j] ] not in threat_candidate:
                            threat_candidate.append( [ [first_i,first_j] , [second_i,second_j] ] )

            t_list = []
            #print('threat_candidate :', threat_candidate)
            if len(threat_candidate) >= 1:
                board.threat_chosen = threat_candidate[0]

        #print('threat_chosen :', board.threat_chosen)

    def predict2(self, board):
        if board.count % 2 == 1:
            board.best_moves.clear()
            board.final_move.clear()
            board.threat_chosen.clear()
            #self.findFinalMoves(board)
            #self.findDefensiveMoves(board)

        if board.final_move != []:
            return board.final_move.pop()
        elif board.threat_chosen != []:
            return board.threat_chosen.pop()
        elif board.best_moves != []:
            return board.best_moves.pop()
        else:
            m1, m2, _ = self.beam_search(board, beam_size=2)
            board.best_moves.append(m2)
            return m1

    def predict(self, board): #without simulation
        if board.count % 2 == 1:
            board.final_move.clear()
            board.threat_chosen.clear()
            self.findFinalMoves(board)
            self.findDefensiveMoves(board)

        if board.final_move != []:
            return board.final_move.pop()
        elif board.threat_chosen != []:
            return board.threat_chosen.pop()
        else:
            max_score = -100
            max_score2 = 0
            max_threat = 0

            for x, y in board.active_area:
                temp = self.evaluate(board, [x, y])
                if temp > max_score:
                    max_score = temp
                    move = [x, y]
        return move

    def threatSearch(self, board, mode=0):

        threat_len = 0
        size = board.size
        state = board.state
        if mode == 1:
            prev = board.prev_mine
            pl_in_turn = 3-board.player_in_turn()
            threat = board.threat_offense
        else :
            prev = board.prev_moves
            pl_in_turn = board.player_in_turn()
            threat = board.threat

        x1, y1 = prev[0]
        x2, y2 = prev[1]

        for x, y in prev:
            for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
                def W(x): return x
                def W2(x): return x
                if dy*(x1-x2) == dx*(y1-y2): #if both stones are on the same line
                    distance = max(abs(x1-x2), abs(y1-y2))
                    opponent = 0
                    if x1 < x2 or (x1 == x2 and y1 < y2):
                        window = list(state[x1+dx*i][y1+dy*i] for i in range(1, distance))
                    else:
                        window = list(state[x2+dx*i][y2+dy*i] for i in range(1, distance))

                    if pl_in_turn in window:
                        opponent += 1
                    if opponent == 0: #if there are no opposing stones between two stones
                        if distance <= 6:
                            def W(x): return x/2
                            def W2(x): return x/2
                        elif distance < 12:
                            def W(x, state={'first_call':True}):
                                if state['first_call']:
                                    state['first_call'] = False
                                    return x-0.5
                                return x
                            def W2(x): return x/2

                t = [] #prevent redundant marks
                for i in range(6): #right to left
                    if x+dx*(-i) >= 0 and x+dx*(-i+5) < size and y+dy*(-i) >= 0 and y+dy*(-i+5) < size and y+dy*(-i) < size and y+dy*(-i+5) >= 0:
                        index = list([x+dx*(-i+j), y+dy*(-i+j)] for j in range(6))
                        index = index[::-1]
                        window = list(state[x][y] for x, y in index)
                        if pl_in_turn not in window and window.count(3 - pl_in_turn) >= 4:
                            empty = list([x, y] for x, y in index if state[x][y] == 0)
                            temp = 0
                            for tx, ty in empty:
                                if [tx, ty] not in t:
                                    #print(tx, ty)
                                    t.append([tx, ty])
                                    threat[tx][ty] += W2(1)
                                    temp = 1
                                else:
                                    break
                            threat_len += W(temp)

                t = []
                for i in range(5,-1,-1): #left to right
                    if x+dx*(-i) >= 0 and x+dx*(-i+5) < size and y+dy*(-i) >= 0 and y+dy*(-i+5) < size and y+dy*(-i) < size and y+dy*(-i+5) >= 0:
                        index = list([x+dx*(-i+j), y+dy*(-i+j)] for j in range(6))
                        window = list(state[x][y] for x, y in index)
                        if pl_in_turn not in window and window.count(3 - pl_in_turn) >= 4:
                            empty = list([x, y] for x, y in index if state[x][y] == 0)
                            for tx, ty in empty:
                                if [tx, ty] not in t:
                                    #print(tx, ty)
                                    t.append([tx, ty])
                                    threat[tx][ty] += W2(1)
                                else:
                                    break

        return threat_len
