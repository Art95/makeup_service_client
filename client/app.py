from flask import Flask
import os
import argparse
from flask_socketio import SocketIO
from client import views
from client.makeup_service_client import MakeupServiceClient
from client.video_streamer import VideoStreamer


app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app, async_mode='threading', always_connect=True)


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="127.0.0.1")
    parse.add_argument('--port', default=5002)
    parse.add_argument('--debug', default=True)

    return parse.parse_args()


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port
    debug = args.debug

    client = MakeupServiceClient("127.0.0.1", 5000)
    video_streamer = VideoStreamer(0)

    socketio.start_background_task(views.send_frames, client, video_streamer)
    print("passed")

    socketio.run(app, host, port, debug=debug)
