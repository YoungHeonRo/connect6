def slidingWindow(board, wb, prev_moves):
    
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
                if board.state[x-i+j][y] == 3-wb:
                    stones_in_window+=1
                elif board.state[x-i+j][y] == 0:
                    empty_idx.append( (x-i+j,y) )
                else :
                    empty_idx.clear()
                    break
            if stone_number >=4 :
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
                if board.state[x][y-i+j] == 3-wb:
                    stones_in_window+=1
                elif board.state[x][y-i+j] == 0:
                    empty_idx.append( (x,y-i+j) )
                else :
                    empty_idx.clear()
                    break
            if stone_number >=4 :
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
                if board.state[x-i+j][y-i+j] == 3-wb:
                    stones_in_window+=1
                elif board.state[x-i+j][y-i+j] == 0:
                    empty_idx.append( (x-i+j,y-i+j) )
                else :
                    empty_idx.clear()
                    break
            if stone_number >=4 :
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
                if board.state[x-i+j][y+i-j] == 3-wb:
                    stones_in_window+=1
                elif board.state[x-i+j][y+i-j] == 0:
                    empty_idx.append( (x-i+j,y+i-j) )
                else :
                    empty_idx.clear()
                    break
            if stone_number >=4 :
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
        return []
    print(max_threat)
    else return defensive_moves




