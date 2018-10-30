def halfMove(board, x,y, wb):
    total_score = 0
    empty = 2
    same = 30

    #+0
    score = 1
    for i in range(1,6):
        if x+i >= board.size :
            break
        elif board.state[x+i][y] == 0 :
            score *= empty 
        elif board.state[x+i][y] == wb :
            score *= same
        else :
            break
    #-0
    for i in range(1,6):
        if x-i < 0 :
            break
        elif board.state[x-i][y] == 0 :
            score *= empty 
        elif board.state[x-i][y] == wb :
            score *= same
        else :
            break
    total_score+=score


    #0+
    score=1
    for i in range(1,6):
        if x+i >= board.size or y+i >= board.size :
            break
        elif board.state[x][y+i] == 0 :
            score *= empty 
        elif board.state[x][y+i] == wb :
            score *= same
        else :
            break
    #0-
    for i in range(1,6):
        if y-i < 0 :
            break
        elif board.state[x][y-i] == 0 :
            score *= empty 
        elif board.state[x][y-i] == wb :
            score *= same
        else : 
            break
    total_score+=score

    #++
    score=1
    for i in range(1,6):
        if x+i >= board.size or y+i >= board.size :
            break
        elif board.state[x+i][y+i] == 0 :
            score *= empty 
        elif board.state[x+i][y+i] == wb :
            score *= same
        else : 
            break
    #--
    for i in range(1,6):
        if x-i < 0 or y-i < 0 :
            break
        elif board.state[x-i][y-i] == 0 :
            score *= empty 
        elif board.state[x-i][y-i] == wb :
            score *= same
        else :
            break  
    total_score+=score

    #+-
    score=1
    for i in range(1,6):
        if x+i >= board.size or y-i < 0 :
            break
        elif board.state[x+i][y-i] == 0 :
            score *= empty 
        elif board.state[x+i][y-i] == wb :
            score *= same
        else : 
            break 
    #-+
    for i in range(1,6):
        if x-i < 0 or y+i >= board.size :
            break
        elif board.state[x-i][y+i] == 0 :
            score *= empty 
        elif board.state[x-i][y+i] == wb :
            score *= same
        else :
            break   
    total_score+=score

    return total_score