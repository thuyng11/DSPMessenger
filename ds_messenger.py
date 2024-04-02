# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import socket
import time
from ds_protocol import create_direct_message, extract_json, request_messages

class DirectMessage:
    '''
    object direct message to store sender name and message and timestamp
    '''
    def __init__(self, recipient, message, timestamp):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    '''
    Connect to server, send message, and retrieve message
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def connect(self):
        '''
        establishes connection with the DS Server using provided credentials
        '''
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
                srv.connect((self.dsuserver, 3021))

                join_msg = '{"join": {"username": "' + self.username + '", "password": "' + self.password + '", "token": ""}}'
                send = srv.makefile('w')
                recv = srv.makefile('r')

                send.write(join_msg + '\r\n')
                send.flush()

                resp = recv.readline()
                if extract_json(resp)[0] == 'error':
                    return False
                return True
        except Exception as e:
            print(f'An error occurred: {e}')

    def send(self, message:str, recipient:str) -> bool:
        '''
        send message to server

        :param message: message to be sent
        :param recipient: username of the recipient
        '''
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
                srv.connect((self.dsuserver, 3021))

                join_msg = '{"join": {"username": "' + self.username + '", "password": "' + self.password + '", "token": ""}}'
                send = srv.makefile('w')
                recv = srv.makefile('r')

                send.write(join_msg + '\r\n')
                send.flush()

                resp = recv.readline()
                if extract_json(resp)[0] == 'error':
                    return False

                self.token = extract_json(resp)[2]

                dm = create_direct_message(self.token, recipient, message, time.time())

                send.write(dm + '\r\n')
                send.flush()

                dm_read = recv.readline()

                if extract_json(dm_read)[0] == 'error':
                    return False
            return True

        except ConnectionError:
            print('An error occurred: Failed to connect to server')
            return False

    def retrieve_new(self) -> list:
        '''request new messages'''
        return self.retrieve_messages('new')

    def retrieve_all(self) -> list:
        '''request all messages'''
        return self.retrieve_messages('all')

    def retrieve_messages(self, message_type: str) -> list:
        '''
        retrieve either new or all message
        :param message_type: new or all
        '''
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
                srv.connect((self.dsuserver, 3021))

                join_msg = '{"join": {"username": "' + self.username + '", "password": "' + self.password + '", "token": ""}}'
                send = srv.makefile('w')
                recv = srv.makefile('r')

                send.write(join_msg + '\r\n')
                send.flush()

                resp = recv.readline()
                if extract_json(resp)[0] == 'error':
                    return False

                self.token = extract_json(resp)[2]

                if self.token is None:
                    return []

                request_json = request_messages(self.token, message_type)
                send.write(request_json + '\r\n')
                send.flush()

                request_read = recv.readline()
                json_tuple = extract_json(request_read)
                if json_tuple[0] == 'error':
                    return False
                direct_messages = []

                for msg in json_tuple[1]:
                    direct_messages.append(DirectMessage(message=msg['message'],
                                                         recipient = msg['from'],
                                                         timestamp= msg['timestamp']))

            return direct_messages
        except ConnectionRefusedError as e:
            raise ConnectionError("Failed to connect to the server") from e
        except TypeError as e:
            raise TypeError('Invalid type') from e
