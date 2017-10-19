import connectfour_tools
import connectfour_functions
import connectfour

from collections import namedtuple

# Host: woodhouse.ics.uci.edu
# Server: 4444

UserAction = namedtuple('UserAction', ['move', 'column_num'])

def read_host() -> str:
    '''
    Asks the user to specify what host they'd like to connect to,
    continuing to ask until a valid answer is given.  An answer is
    considered valid when it consists of something other than just
    spaces.
    '''

    while True:
        host = input('Host: ').strip()

        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host


def read_port() -> int:
    '''
    Asks the user to specify what port they'd like to connect to,
    continuing to ask until a valid answer is given.  A port must be an
    integer between 0 and 65535.
    '''

    while True:
        try:
            port = int(input('Port: ').strip())

            if port < 0 or port > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return port

        except ValueError:
            print('Invalid; please try again. ')
            
           
def username() -> str:
    ''' Asking for the username '''
    while True:
        name = input('Enter your username: ').strip()
        user_name = name.split()
        if len(user_name) == 1:
            return name
        
        
def action() -> str:
    ''' Handling user inputs '''
    move = connectfour_functions.ask_action()
    column_num = str(connectfour_functions.ask_move())
    result = move + ' ' + column_num
    return result


def get_action(move:str) -> UserAction:
    ''' Puts the move into a namedtuple '''
    result = move.split()
    return UserAction(move = result[0], column_num = int(result[1]))
          

def make_connection() -> 'GameConnection':
    ''' Creates the connection '''
    host = read_host()
    port = read_port()
    print('Connecting to {} on port {} ...'.format(host, port))
    return connectfour_tools.connect(host, port)

def closing_all_connection(connection:'connection') -> None:
    '''closes the connection'''
    
    print('Closing Connection...')
    connectfour_tools.close(connection)
    print('Connection Closed! ')
    

def game():
    ''' Plays the game '''
    game_state = connectfour.new_game()
    try:
        connection = make_connection()
    except:
        print('CONNECTION FAILED')
        return None
    try: 
        user_name = username()
        if connectfour_tools.get_server(connection, user_name) == connectfour_tools.WELCOME:
            request = connectfour_tools.request_game(connection) # READY
            if request == connectfour_tools.READY:
            
                while connectfour.winner(game_state) == connectfour.NONE:
                    move = action()
                    user_move = get_action(move)
                    game_state = connectfour_functions.action(user_move.move,user_move.column_num,game_state)
                    connectfour_tools.send_message(connection, move)
                    connectfour_functions.board(game_state)
                    print()
                    check = connectfour_tools.receive_response(connection)
     
                    if check == 'OKAY':
                        move = connectfour_tools.receive_response(connection)
                        if 'DROP' in move or 'POP' in move :
                            server_move = get_action(move)
                            game_state = connectfour_functions.action(server_move.move,server_move.column_num,game_state)
                            connectfour_functions.board(game_state)
                            r = connectfour_tools.receive_response(connection)
                        if r == 'WINNER_RED':
                            print('WINNER_RED')
                            closing_all_connection(connection)
                        elif r == 'WINNER_YELLOW':
                            print('WINNER_YELLOW')
                            closing_all_connection(connection)
                        
                        elif r == 'READY':
                            pass
                        else:
                            closing_all_connection(connection)
                            break
                    elif check == 'INVALID':
                        print('INVALID MOVE')
                        move = action()
                        user_move = get_action(move)
                        game_state = connectfour_functions.action(user_move.move,user_move.column_num,game_state)
                        connectfour_tools.send_message(connection, move)
                        connectfour_functions.board(game_state)
                    elif check == connectfour_tools.ERROR or check == connectfour_tools.NO_USER:
                        closing_all_connection(connection)
                        break

        else:
     
            print('CONNECTION FAILED')
            connectfour_tools.close(connection)
            
    except connectfour.InvalidMoveError:
        print('INVALID MOVE')
    except connectfour_tools.ConnectFourError:

        print('CONNECTION FAILED')
        connectfour_tools.close(connection)

    
if __name__ == '__main__':
    game()

    
