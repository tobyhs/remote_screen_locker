import os
from unittest import TestCase, mock

from remote_screen_locker.middleware import AuthMiddleware

class AuthMiddlewareTest(TestCase):
    def setUp(self):
        self.app = mock.Mock(name='app')
        self.start_response = mock.Mock(name='start_response')
        self.correct_token = 'X7Y8Z9'
        os.environ['REMOTE_SCREEN_LOCKER_TOKEN'] = self.correct_token
        self.middleware = AuthMiddleware(self.app)

    def test_call_with_correct_token(self):
        environ = {'HTTP_X_TOKEN': self.correct_token}
        self.app.return_value = [b'{}']
        self.assertEqual(self.middleware(environ, self.start_response), [b'{}'])
        self.app.assert_called_once_with(environ, self.start_response)

    def test_call_with_wrong_token(self):
        environ = {'HTTP_X_TOKEN': 'wrong'}
        self.assertEqual(self.middleware(environ, self.start_response), [])
        self.start_response.assert_called_once_with('401 Unauthorized', [])
