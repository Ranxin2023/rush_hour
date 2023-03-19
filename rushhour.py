import copy
car_set=set()
car_dir=dict()
car_pos=dict()
car_type=dict()
solution=list()
all_states=list()
all_fn=list()
def rushhour(heu_num, list_str):
    board=store_in_board(list_str)
    #print(board)
    store_information(board)
    all_states.append([(board,None)])
    all_fn.append([calculate_blocking_heu_num(board)])
    #print(calculate_blocking_heu_num(board))
    blocking_heuristic_layer(heu_num)
    '''
    new_states=generate_new_states(board)
    for each in new_states:
        print(each)
    '''
#This function is to calculate the value of blocking hieuristic value
#We calculate the hieuristic number by counting the number of letter in front of car x
def calculate_blocking_heu_num(board):
    front_x=int()
    heu_num=0
    for i in range(6):
        if board[2][i]=='X':
            #print('i',i)
            front_x=i
            front_x+=1
            break
    #print(front_x)
    if front_x==5:
        return heu_num
    for i in range((front_x+1),6):
        if board[2][i]!='-':
            heu_num+=1
    return heu_num

def blocking_heuristic_layer(heu_num):
    
    moves=0
    while True:
        all_states.append(list())
        all_fn.append(list())
        for state_tup in all_states[moves]:
            state=copy.deepcopy(state_tup[0])
            new_states=generate_new_states(state)
            print(new_states)
            for new_state in new_states:
                all_states[moves+1].append((new_state, state))
                if calculate_blocking_heu_num(new_state)==heu_num:
                    return (new_state,moves+1)
                all_fn[moves+1].append(calculate_blocking_heu_num(new_state)+moves+1)
            new_states.clear()
        min_fn=min(all_fn[moves+1])
        count=0
        for i in range(len(all_fn[moves+1])):
            if all_fn[moves+1][i]!=min_fn:
                all_states[moves+1].remove(all_states[moves+1][i-count])
            count+=1
        print(len(all_states[moves+1]))
        #print('new state',len(new_states))
        moves+=1
            
'''
def backtracking(final, origin):
'''
#This function is for generating all the states based on the state of board now
def generate_new_states(board):
    new_states=list()
    for car in car_set:
        car_coor=car_pos[car]
        #move horizontally
        if car_dir[car]=='h':
            #car
            if car_type[car]=='c':
                #move right
                if car_coor[1]<4:
                    if board[car_coor[0]][car_coor[1]+2]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0], car_coor[1], car_coor[0], car_coor[1]+2)
                        new_states.append(board_copy)
                #move left
                if car_coor[1]>0:
                    if board[car_coor[0]][car_coor[1]-1]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0], car_coor[1]+1, car_coor[0], car_coor[1]-1)
                        new_states.append(board_copy)
            #truck
            if car_type[car]=='t':
                if car_coor[1]<3:
                    if board[car_coor[0]][car_coor[1]+3]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0], car_coor[1], car_coor[0], car_coor[1]+3)
                        new_states.append(board_copy)
                if car_coor[1]>0:
                    if board[car_coor[0]][car_coor[1]-1]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0], car_coor[1]+2, car_coor[0], car_coor[1]-1)
                        new_states.append(board_copy)
        #move vertically
        if car_dir[car]=='v':
            #car
            if car_type[car]=='c':
                #move right
                if car_coor[0]<4:
                    if board[car_coor[0]+2][car_coor[1]]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0], car_coor[1], car_coor[0]+2, car_coor[1])
                        new_states.append(board_copy)
                #move left
                if car_coor[0]>0:
                    if board[car_coor[0]-1][car_coor[1]]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0]+1, car_coor[1], car_coor[0]-1, car_coor[1])
                        new_states.append(board_copy)
            #truck
            if car_type[car]=='t':
                if car_coor[0]<3:
                    if board[car_coor[0]+3][car_coor[1]]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0], car_coor[1], car_coor[0]+3, car_coor[1])
                        new_states.append(board_copy)
                if car_coor[0]>0:
                    if board[car_coor[0]-1][car_coor[1]]=='-':
                        board_copy=copy.deepcopy(board)
                        swap_board(board_copy, car_coor[0]+2, car_coor[1], car_coor[0]-1, car_coor[1])
                        new_states.append(board_copy)
        
    return new_states
    
#This function stores all the information of the car
#including: the name of the car, the position of the car, and the type of the car.
def store_information(board):
    for i in range(6):
        for j in range(6):
            if board[i][j]!='-':
                car=board[i][j]  
                if car not in car_set:
                    car_set.add(car)
                    car_pos[car]=(i,j)
                    if i!=5 and board[i+1][j]==car:
                        car_dir[car]='v'
                        if i<4 and board[i+2][i]==car:
                            car_type[car]='t'
                        else:
                            car_type[car]='c'
                    if j!=5 and board[i][j+1]==car:
                        car_dir[car]='h'
                        if j<4 and board[i][j+2]==car:
                            car_type[car]='t'
                        else:
                            car_type[car]='c'

#This function is for moving the car
#swaping the position of the car letter and the character '-' will move the car
def swap_board(board, co1_x, co1_y, co2_x, co2_y):
    board[co1_x][co1_y], board[co2_x][co2_y]=board[co2_x][co2_y], board[co1_x][co1_y]

#store the list into the type of board
def store_in_board(list_str):
    board=list()
    for i in range(len(list_str)):
        board.append(list())
        for j in range(len(list_str[i])):
            board[i].append(list_str[i][j])
    return board

def main():
    rushhour(0, ["--B---","--B---","XXB---","--AA--","------","------"])
    '''
    for c in car_pos.items():
        print(c, end='')
    '''

if __name__ == "__main__":
    main()


        
    
