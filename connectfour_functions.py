import connectfour
        
def ask_action() -> str:
    '''asks the user whether they want to pop or drop'''
    while True:
        user = input("Do you want to 'pop' or 'drop'? ").upper().strip()
        if user == 'DROP':
             return user
        elif user == 'POP':
            return user
        else:
            print('INVALID MOVE')
            

def ask_move() -> int:
    '''asks user what column the want to put the game piece in'''
    
    while True:
        move = int(input('Which column do you want to put it in? '))
        if move >= 1 and move <= 7:
            return move
        else:
            print('INVALID MOVE')
            
def action( move: str, column_num: int, game_state: 'GameState') -> 'GameState':
    '''implements pop or drop'''

    if move == 'DROP':
        return connectfour.drop(game_state, column_num -1 )
        
    elif move == 'POP':
        return connectfour.pop(game_state, column_num -1)
    
def get_winner(game_state: 'Gamestate') -> None:
    if connectfour.winner(game_state) == 1:
        print('WINNER_RED')
    elif connectfour.winner(game_state) == 2:
        print('WINNER_YELLOW')
        
def board(game_state: 'GameState') -> None:
    '''prints the board'''
    for number in range(connectfour.BOARD_COLUMNS):
        print(' ' + str(number + 1) + ' ',end=' ')
    print()
    
    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS):
            if game_state.board[col][row] == 0:
                print(' . ', end=' ')
            elif game_state.board[col][row] == 1:
                print(' R ', end=' ')
            else:
                print(' Y ', end=' ')
        print()
