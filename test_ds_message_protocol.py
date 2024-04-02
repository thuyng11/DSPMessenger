# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import unittest
import json
from ds_protocol import create_direct_message, extract_json, DirectMessage

class TestDSProtocol(unittest.TestCase):
    '''
    Unit Test for ds_protocol functions
    '''

    def test_create_direct_message(self):
        '''
        test create direct message
        '''
        token = "test_token"
        recipient = "test_recipient"
        message = "Hello, World!"
        timestamp = "2023-04-01T12:00:00Z"

        expected_json = json.dumps({
            "token": token,
            "directmessage": {
                "entry": message,
                "recipient": recipient,
                "timestamp": timestamp
            }
        })

        result_json = create_direct_message(token, recipient, message, timestamp)
        self.assertEqual(result_json, expected_json,
                        "Invalid format")

    def test_extract_json_valid_single(self):
        '''
        test extract_json with single json object
        '''
        json_msg = json.dumps({
            "response": {
                "type": "ok",
                "message": "Message content",
                "token": "example_token"
            }
        })

        expected_result = DirectMessage(type='ok',
                                        message='Message content',
                                        token='example_token')

        result = extract_json(json_msg)
        self.assertEqual(result, expected_result,
                         "extract_json does not correctly parse a valid JSON message.")
        self.assertIsInstance(result, type(expected_result),
                            "Should return a namedtupled of messages for a valid JSON list response.")

if __name__ == '__main__':
    unittest.main()
