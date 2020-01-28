from unittest import TestCase, mock

from remote_screen_locker import screen

class ScreenTest(TestCase):
    def test_is_locked_false(self):
        with mock.patch('Quartz.CGSessionCopyCurrentDictionary') as session_patch:
            session_patch.return_value = {}
            self.assertFalse(screen.is_locked())

    def test_is_locked_true(self):
        with mock.patch('Quartz.CGSessionCopyCurrentDictionary') as session_patch:
            session_patch.return_value = {'CGSSessionScreenIsLocked': True}
            self.assertTrue(screen.is_locked())

    def test_lock(self):
        with mock.patch('subprocess.check_call') as call_patch:
            screen.lock()
            call_patch.assert_called_once_with([
                'osascript',
                '-e',
                'tell application "System Events" to keystroke "q" using {control down, command down}',
            ])
