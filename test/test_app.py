from bottle import HTTPResponse
import bottle
import io
import json
from unittest import TestCase, mock
from typing import Dict

from remote_screen_locker import app
from remote_screen_locker.middleware import AuthMiddleware

class AppTest(TestCase):
    def setUp(self):
        super().setUp()
        bottle.request.bind({})

    def test_get_screen_locked(self):
        with mock.patch('remote_screen_locker.screen.is_locked') as is_locked_patch:
            is_locked_patch.return_value = True
            self.assertEqual(app.get_screen(), {'locked': True})

    def test_get_screen_unlocked(self):
        with mock.patch('remote_screen_locker.screen.is_locked') as is_locked_patch:
            is_locked_patch.return_value = False
            self.assertEqual(app.get_screen(), {'locked': False})

    def test_patch_screen_locked_true(self):
        self._set_json_request_body({'locked': True})
        with mock.patch('remote_screen_locker.screen.lock') as lock_patch:
            self.assertEqual(app.patch_screen(), {'locked': True})
            lock_patch.assert_called_once()

    def test_patch_screen_locked_false(self):
        self._set_json_request_body({'locked': False})
        self._check_http_response(
            app.patch_screen(),
            400,
            {'error': 'locked cannot be false'},
        )

    def test_patch_screen_no_request_body(self):
        self._check_http_response(
            app.patch_screen(),
            400,
            {'error': 'Invalid request content type'},
        )

    def test_app(self):
        self.assertIsInstance(app.app, AuthMiddleware)
        self.assertIs(app.app.app, bottle.app())

    def _set_json_request_body(self, body):
        raw_body = json.dumps(body).encode()
        environ = {
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': len(raw_body),
            'wsgi.input': io.BytesIO(raw_body)
        }
        bottle.request.bind(environ)

    def _check_http_response(
        self,
        http_response: HTTPResponse,
        expected_status_code: int,
        expected_body: Dict[str, object]
    ) -> None:
        """Checks the given HTTP response

        Args:
            http_response: the HTTP response to check
            expected_status: the expected HTTP status code
            expected_body: the expected JSON body
        """
        self.assertIsInstance(http_response, HTTPResponse)
        self.assertEqual(http_response.status_code, expected_status_code)
        self.assertEqual(http_response.body, expected_body)
