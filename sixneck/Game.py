from Player import *
from Board import *

#고정값
black = 1
white = 2
size = 19

#임의로 설정하는 값
player1 = init_player(black, 'human')
player2 = init_player(white, 'rb')

#게임 시작
try:
    board = Board(size)
    board.update(9, 9, black) #흑팀의 첫수는 정중앙에 놓는다. 
    prev_moves=[]
    while True:
        temp_moves = []
        #누구의 턴인가?
        if board.count % 4 == 0 or board.count % 4 == 3:
            player = player1
        else:
            player = player2

        if player.color == 'rb':
            defensive_moves = player.threatMove(board, player.color, prev_moves)
        else :
            defensive_moves = []

        print(defensive_moves)
        #first move
        x, y = first_move = player.get_move(board, defensive_moves)
        temp_moves.append( (x,y) )
        is_end, winner = board.update(x, y)
        if is_end:(
            if winner == -1:
                print('draw')
            else:
                print('winner is player', winner)
            break
        #second move
        x, y = second_move = player.get_move(board, defensive_moves)
        temp_moves.append( (x,y) )

        is_end, winner = board.update(x, y)
        prev_moves = temp_moves
        board.changeColor();
        
        if is_end:
            if winner == -1:
                print('draw')
            else:
                print('winner is player', winner)
            break
        
except KeyboardInterrupt:
    print('\nbye')




