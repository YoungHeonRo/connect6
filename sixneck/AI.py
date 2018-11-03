def predict(board):
    if board.count % 2 == 1:
        threatSearch(board)
    size = board.size
    state = board.state

    defensive_moves = []
    for i in range(size):
        for j in range(size):
            if [i, j] in board.available_moves and board.threat[i][j] >= 2:
                defensive_moves.append([i, j, board.threat[i][j]])

    defensive_moves.sort(key=lambda a:a[-1], reverse=True)
    defensive_moves = [[i,j] for i,j,k in defensive_moves]
    if len(defensive_moves) >= 1:
        move = defensive_moves[0]
    else:
        max_score = 0
        for x, y in board.available_moves:
            temp = halfMove(board, x, y)
            if temp > max_score:
                max_score = temp
                move = [x, y]

    return move

def halfMove(board, x, y):
    size = board.size
    state = board.state

    empty = 2
    own = 2
    exp = 13
    W_degree = [1.0, 1.00000181862, 1.00000363725, 1.00000726562]

    total_score = 0
    total_degree = 0
    for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
        score = 1
        degree = 1
        for l in [-1, 1]:
            for k in range(1,6):
                if x+dx*l*k >= size or x+dx*l*k < 0 or y+dy*l*k >= size or y+dy*l*k < 0:
                    break
                elif state[x+dx*l*k][y+dy*l*k] == 0:
                    score *= empty
                elif state[x+dx*l*k][y+dy*l*k] == board.player_in_turn():
                    score *= own**(exp-k)
                else:
                    degree = 0
                    break
        total_degree += degree
        total_score += score

    return W_degree[degree - 1] * total_score

def threatSearch(board):
    size = board.size
    state = board.state
    for x, y in board.prev_moves:
        for dx, dy in [[1,0], [0,1], [1,1], [1,-1]]:
            for i in range(6):
                if x+dx*(-i) >= 0 and x+dx*(-i+5) < size and y+dy*(-i) >= 0 and y+dy*(-i+5) < size and y+dy*(-i) < size and y+dy*(-i+5) >= 0:
                    index = list([x+dx*(-i+j), y+dy*(-i+j)] for j in range(6))
                    window = list(state[x][y] for x, y in index)
                    if board.player_in_turn() not in window and window.count(3 - board.player_in_turn()) >= 4:
                        empty = list([x, y] for x, y in index if state[x][y] == 0)
                        for tx, ty in empty:
                            board.threat[tx][ty] += 1
