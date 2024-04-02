# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import json
from pathlib import Path


"""
DsuFileError is a custom exception handler that
you should catch in your own code. It
is raised when attempting to load or save
Profile objects to file the system.
"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception
handler that you should catch in your own code.
It is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    '''DSU Profile Error'''
    pass



class Profile1:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You 
    will need to use this class to manage the information provided by each new user 
    created within your program for a2. Pay close attention to the properties and 
    functions in this class as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the properties 
    exposed by this class. A Profile class should ensure that a username and password 
    are set, but contains no conventions to do so. You should make sure that your code 
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = ''            # OPTIONAL
        self._posts = []         # Not available
        self._message = []       # List of dictionary {username: str, message: []}
        self._friends = []        # Storing friends' usernames
        self._sender = []        # List of dictionary {recipient: str, message:[]} of messages that the USER sent to other users

    def add_messages(self, sender: str, recipient: str, message: str, timestamp: float) -> None:
        '''
        add new json object to the local storage for message
        '''
        message_dict = {'sender': sender,
                        'recipient': recipient,
                        'message': message,
                        'timestamp': timestamp}
        self._message.append(message_dict)


    def get_messages(self) -> dict:
        '''
        retrieve all stored messages
        '''
        return self._message

    def add_friend(self, sender: str) -> None:
        '''
        add new username to the local storage for message
        '''
        if sender not in self._friends:
            self._friends.append(sender)

    def get_friends(self) -> list[str]:
        '''
        retrieve list of all friend usernames
        '''
        return self._friends

    def add_user_message(self, sender, recipient, message, timestamp) -> None:
        '''
        add sender message
        '''
        sender_dict = {'sender': sender,
                       'recipient': recipient,
                       'message': message,
                       'timestamp': timestamp}
        self._sender.append(sender_dict)

    def get_user_message(self) -> list[dict]:
        '''
        get sender message
        '''
        return self._sender

    def save_profile(self, path: str) -> None:
        '''
        save profile for user
        :param path: file path to save
        '''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                data = {
                    "dsuserver": self.dsuserver,
                    "username": self.username,
                    "password": self.password,
                    "bio": self.bio,
                    "_posts": self._posts,
                    "_messages": self._message,  # Serialize DirectMessage objects
                    "_friends": self._friends,
                    "_sender": self._sender
                }
                json.dump(data, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        '''load_profile will populate the current 
        instance of Profile with data stored in a 
        DSU file.
        :param path: file path to load profile'''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self._message = obj.get( '_messages', [])
                self._friends = obj.get('_friends', [])
                self._sender = obj.get('_sender', [])
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
