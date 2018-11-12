import copy

def findFinalMoves(board):
    offensive_threat = threatSearch(board, 1)
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
                    b.update(first_i, first_j)
                    b.update(second_i, second_j)
                    if b.get_winner() > 0 :
                        board.final_move = [ [first_i, first_j], [second_i, second_j] ]
    return None

def findDefensiveMoves(board):
    size = board.size
    state = board.state

    threat_len = threatSearch(board)
    print('threat_len :', threat_len)

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
            temp_threat_len = threatSearch(temp_board)
            if temp_threat_len == 0:
                threat_candidate.append( [one_i, one_j] )

        if len(threat_candidate) == 1:
            board.threat_chosen.append( threat_candidate[0] )
        elif len(threat_candidate) >= 2:
            board.threat_chosen = getMoveList(board, threat_candidate, 1)

    elif threat_len >= 2:
        #defensive moves : i, j, threat value
        for first_i, first_j in defensive_moves :
            for second_i, second_j in defensive_moves :
                if (first_i*board.size+first_j) > (second_i*board.size+second_j) :
                    temp_board = copy.deepcopy(board)
                    temp_board.state[first_i][first_j] = temp_board.player_in_turn()
                    temp_board.state[second_i][second_j] = temp_board.player_in_turn()
                    temp_threat_len = threatSearch(temp_board)
                    if temp_threat_len == 0 and [ [second_i, second_j] , [first_i,first_j] ] not in threat_candidate:
                        threat_candidate.append( [ [first_i,first_j] , [second_i,second_j] ] )

        t_list = []
        print('threat_candidate :', threat_candidate)
        if len(threat_candidate) == 1:
            board.threat_chosen = threat_candidate[0]
        elif len(threat_candidate) >= 2:
            temp_list = []
            for idx, one_list in enumerate(threat_candidate):
                tx1, ty1 = one_list[0]
                tx2, ty2 = one_list[1]
                t_value = halfMove(board, tx1, ty1) + halfMove(board, tx2, ty2)
                temp_list.append( [t_value, idx] )
            temp_list.sort(key = lambda a:a[0], reverse=True)

            board.threat_chosen = threat_candidate[ temp_list[0][1] ]

    print('threat_chosen :', board.threat_chosen)

def predict(board):
    if board.count % 2 == 1:
        findFinalMoves(board)
        findDefensiveMoves(board)

    if board.final_move != []:
        return board.final_move.pop()

    if board.threat_chosen != []:
        return board.threat_chosen.pop()
    else:
        max_score = 0
        max_score2 = 0
        max_threat = 0

        x1, y1 = board.prev_moves[0]
        x2, y2 = board.prev_moves[1]
        for x, y in board.available_moves:
            #defensive_strategy
            #if (abs(x-x1) <= 2 and abs(y-y1) <= 2) or (abs(x-x2) <= 2 and abs(y-y2) <= 2):
            if True:
                """
                temp_board = copy.deepcopy(board)
                temp_board.state[x][y] = temp_board.player_in_turn()
                if threatSearch(temp_board, 1) >= max_threat :
                """
                temp = halfMove(board, x, y)
                if temp > max_score:
                    max_score = temp
                    move = [x, y]

        for x, y in board.available_moves:
            #defensive_strategy
            #if (abs(x-x1) <= 2 and abs(y-y1) <= 2) or (abs(x-x2) <= 2 and abs(y-y2) <= 2):
            if True:
                temp = halfMove(board, x, y, 1)
                """
                temp_board = copy.deepcopy(board)
                temp_board.state[x][y] = 3-temp_board.player_in_turn()
                temp_threat = threatSearch(temp_board)
                if  temp_threat > 2 :
                """
                if temp > max_score:
                    max_score = temp
                    move = [x, y]

    return move

'''def simulate(board, move_list):
    b = copy.deepcopy(board)
    for move in move_list:
    b.update(move)
    t = threatSearch(b)
    return t'''

def getMoveList(board, xy_list, n):
    xy_score_list = []
    for x, y in xy_list:
        score = halfMove(board, x, y)
        xy_score_list.append([x, y, score])
    xy_score_list.sort(key=lambda a:a[-1], reverse=True)
    move_list = list([xy[0], xy[1]] for xy in xy_score_list)
    return move_list[:n]

def halfMove(board, x, y, mode=0):
    size = board.size
    state = board.state

    empty = 2
    own = 2
    exp = 13 #6
    W_degree = [1.0, 1.00000181862, 1.00000363725, 1.00000726562]

    if mode == 1:
        pl_in_turn = 3-board.player_in_turn()
    else :
        pl_in_turn = board.player_in_turn()

    total_score = 0
    total_degree = 0
    for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
        score = 1
        degree = 1
        total_distance = 0
        for l in [-1, 1]:
            distance = 6
            for k in range(1,6):
                if x+dx*l*k >= size or x+dx*l*k < 0 or y+dy*l*k >= size or y+dy*l*k < 0:
                    distance = k
                    break
                elif state[x+dx*l*k][y+dy*l*k] == 0:
                    score *= empty
                elif state[x+dx*l*k][y+dy*l*k] == pl_in_turn:
                    score *= own**(exp-k)
                else:
                    degree = 0
                    distance = k
                    break
            total_distance += distance

        total_degree += degree
        if total_distance > 6:
            total_score += score

    return W_degree[degree - 1] * total_score

def threatSearch(board, mode=0):

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
