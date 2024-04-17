from bottle import HTTPResponse, get, request, route
import bottle
from typing import Dict

from remote_screen_locker import screen
from remote_screen_locker.middleware import AuthMiddleware

@get('/screen')
def get_screen() -> Dict[str, object]:
    """Gets the lock status of the screen."""
    return {'locked': screen.is_locked()}

@route('/screen', 'PATCH')
def patch_screen() -> Dict[str, object]:
    """Updates the lock status of the screen.

    This currently only supports locking (not unlocking) the screen remotely.
    You need to provide a JSON request body like `{"locked": true}`.
    """
    if request.json:
        if request.json.get('locked'):
            screen.lock()
            return {'locked': True}
        else:
            return HTTPResponse({'error': 'locked cannot be false'}, 400)
    else:
        return HTTPResponse({'error': 'Invalid request content type'}, 400)

app = AuthMiddleware(bottle.app())
