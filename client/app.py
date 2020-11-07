from flask import Flask
import os
import argparse
import time
from flask_socketio import SocketIO
from client.makeup_service_client import MakeupServiceClient
from client.video_streamer import VideoStreamer
from client.makeup_applier import MakeupApplier


app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app, async_mode='threading', always_connect=True)


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="127.0.0.1")
    parse.add_argument('--port', default=5002)
    parse.add_argument('--debug', default=True)

    return parse.parse_args()


def provide_images(client, video_streamer, makeup_applier, fps):
    while True:
        ret, image = video_streamer.get_frame()

        if ret:
            client.send_image(image)
            makeup_applier.put_image(image)

        time.sleep(1.0 / fps)


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port
    debug = args.debug

    client = MakeupServiceClient("127.0.0.1", 5000)
    video_streamer = VideoStreamer(0)
    makeup_applier = MakeupApplier()
    fps = 2

    socketio.start_background_task(provide_images, client, video_streamer, makeup_applier, fps)
    socketio.start_background_task(makeup_applier.run)
    print("passed")

    socketio.run(app, host, port, debug=debug)
