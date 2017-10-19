import socket

from collections import namedtuple

NO_USER = 0 
OKAY = 1
READY = 2
WELCOME = 3 
ERROR = 4

GameConnection = namedtuple('GameConnection', ['socket', 'input', 'output'])

class ConnectFourError(Exception):
    pass

def connect(host: str, port: int) -> 'connection':
    '''
    Connects to the echo server, which is assumed to be running on the
    given host and listening on the given port.  If successful, a
    connection object is returned; if unsuccessful, an exception is
    raised.
    '''
    echo_socket = socket.socket()
    echo_socket.connect((host, port))
    echo_socket_input = echo_socket.makefile('r')
    echo_socket_output = echo_socket.makefile('w')
    return GameConnection(socket = echo_socket, 
                          input = echo_socket_input, 
                          output = echo_socket_output)


def close(connection: GameConnection) -> None:
    '''
    Closes a connection
    '''

    connection.input.close()
    connection.output.close()
    connection.socket.close()


def get_server(connection:GameConnection, username:str) -> int:
    ''' Request a server '''
    connection.output.write('I32CFSP_HELLO' + ' ' + username +'\r\n') 
    connection.output.flush()
    response = receive_response(connection)
    if response == 'WELCOME' + ' ' + username:
        print('WELCOME ' + username)
        return WELCOME
    elif response.startswith('NO_USER'):
        return NO_USER
    elif response.startswith('ERROR'):
        return ERROR
    else:
        raise ConnectFourError
    

def request_game(connection:GameConnection) -> int:
    ''' Requests the game '''
    send_message(connection, 'AI_GAME')
    if receive_response(connection) == 'READY':
        return READY
    else:
        return NO_USER
        
def send_message(connection: GameConnection, message: str) -> None:
    '''
    Sends a message to the echo server via a connection that is already
    assumed to have been opened (and not yet closed).
    '''

    connection.output.write(message + '\r\n')
    connection.output.flush()
    
    
def receive_response(connection: GameConnection) -> str:
    '''
    Receives a response from the echo server via a connection that is
    already assumed to have been opened (and not yet closed).
    '''
    return connection.input.readline()[:-1]
        
