# Remote Screen Locker

This is a web app for macOS that serves an HTTP API to:
* check whether the screen is locked 
* lock the screen

## Setup

Install Python 3 (I used `brew install python`) and run the following from the
project root:
```sh
python3 -v venv venv
. venv/bin/activate
pip install -r requirements.txt
```

To start the app, run:
```sh
REMOTE_SCREEN_LOCKER_TOKEN=secret gunicorn remote_screen_locker.app:app
```

To run tests:
```sh
python -m unittest
```

## API

For authentication, set the `REMOTE_SCREEN_LOCKER_TOKEN` environment variable
to the desired token when running the app. Provide an `X-Token` header with the
token for requests.

To get the screen status:
```sh
$ curl -H 'X-Token: secret' localhost:8000/screen
{"locked": false}
```

To lock the screen:
```sh
$ curl -H 'X-Token: secret' -H 'Content-Type: application/json' -X PATCH -d '{"locked": true}' localhost:8000/screen
{"locked": true}
```
