from flask import Flask
import os
import argparse
from flask_socketio import SocketIO
from client import views


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/video_feed', view_func=views.video_feed)

socketio = SocketIO(app)
socketio.on_event('segmentation', views.receive_segmentation)


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="127.0.0.1")
    parse.add_argument('--port', default=5001)
    parse.add_argument('--debug', default=True)

    return parse.parse_args()


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port
    debug = args.debug

    socketio.run(app, host, port, debug=debug)
