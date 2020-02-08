# Remote Screen Locker

This is a web app for macOS that serves an HTTP API to:
* check whether the screen is locked 
* lock the screen

## Setup

Install Python 3 (I used `brew install python`) and run the following from the
project root:
```sh
virtualenv -p /usr/local/bin/python3 venv
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
