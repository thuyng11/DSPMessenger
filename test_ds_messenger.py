# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import unittest
from unittest.mock import patch
from ds_messenger import DirectMessenger

class TestDirectMessenger(unittest.TestCase):
    '''
    Test sucessful cases for sending, retrieving new, and retrieving all messages
    '''

    def setUp(self):
        self.dsuserver = "168.235.86.101"
        self.username = "sallie"
        self.password = "password123"
        self.messenger = DirectMessenger(dsuserver=self.dsuserver,
                                         username=self.username,
                                         password=self.password)

    @patch('ds_messenger.requests.post')
    def test_send_success(self, mock_post):
        '''
        testing if semd_message function successfully send message to server

        :param mock_post: test post
        '''
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": {"type": "ok", "message": "Direct message sent"}}

        message = "Hello, World!"
        recipient = "chip"
        result = self.messenger.send(message=message, recipient=recipient)
        self.assertTrue(result, "Sending message should return True on success")


    @patch('ds_messenger.requests.post')
    def test_retrieve_new(self, mock_post):
        '''
        Mocking retrieval of new messages

        :param mock_post: test post
        
        '''
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "type": "ok",
                "messages": [
                    {"message": "Test Message 1", "from": "user1", "timestamp": "1234567890.123456"},
                    {"message": "Test Message 2", "from": "user2", "timestamp": "1234567891.123456"}
                ]
            }
        }

        messages = self.messenger.retrieve_new()
        self.assertIsInstance(messages, list, "Message should be a list")

    @patch('ds_messenger.requests.post')
    def test_retrieve_all(self, mock_post):
        '''
        Mocking retrieval of all messages

        :param mock_post: test post
        
        '''
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "type": "ok",
                "messages": [
                    {"message": "Test Message 1", "from": "user1", "timestamp": "1234567890.123456"}
                ]
            }
        }

        messages = self.messenger.retrieve_all()
        self.assertIsInstance(messages, list, "Message should be a list")

class TestSendFailure(unittest.TestCase):
    '''
    Test failure cases for sending messages
    '''
    def setUp(self):
        self.dsuserver = "168.23gdgtgd1"
        self.username = "hjfgeiuygfw"
        self.password = "fasdgfdusykgfs"
        self.messenger = DirectMessenger(dsuserver=self.dsuserver,
                                         username=self.username,
                                         password=self.password)

    @patch('ds_messenger.requests.post')
    def test_send_failure(self):
        '''
        testing failure message where username and server info is incorrect
        '''
        message = "Hello, World!"
        recipient = "another_user"
        result = self.messenger.send(message=message, recipient=recipient)
        self.assertFalse(result, "Sending message should return False on failure")


if __name__ == "__main__":
    unittest.main()
