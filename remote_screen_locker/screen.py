"""
Defines functions related to locking the screen.
"""

import subprocess

import Quartz

def is_locked() -> bool:
    """Checks whether the screen is locked.

    Returns:
        whether the screen is locked
    """
    session = Quartz.CGSessionCopyCurrentDictionary()
    return session.get('CGSSessionScreenIsLocked', False)

def lock() -> None:
    """Locks the screen."""
    subprocess.check_call([
        'osascript',
        '-e',
        'tell application "System Events" to keystroke "q" using {control down, command down}',
    ])
