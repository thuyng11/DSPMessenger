# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import json
from collections import namedtuple

DirectMessage = namedtuple('DirectMessage', ['type', 'message', 'token'])


def create_direct_message(token: str, recipient: str, message: str, timestamp: str) -> str:
    """
    Creates a JSON string for sending a direct message to another user.
    """
    direct_message = {
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": timestamp
        }
    }
    return json.dumps(direct_message)


def request_messages(token: str, message_type: str = "new") -> str:
    """
    Creates a JSON string for requesting messages from the server.
    """
    return json.dumps({
        "token": token,
        "directmessage": message_type
    })


def extract_json(json_msg: str) -> DirectMessage:
    '''
    extract json message and return a tuple of direct message
    :param json_msg: A JSON formatted string of message
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get('response', {})
        response_type = response.get('type',  '')
        response_token = response.get('token', '')

        if 'message' in response:
            response_message = response.get('message', '')

        elif 'messages' in response:
            response_message = []

            for msg in response.get('messages'):
                response_message.append(msg)

        return DirectMessage(response_type, response_message, response_token)


    except json.JSONDecodeError:
        print("Json cannot be decoded.")
