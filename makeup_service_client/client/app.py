from flask import Flask
import os
import cv2
import argparse
import time
from flask_socketio import SocketIO
from makeup_service_client.client.makeup_client import MakeupServiceClient
from makeup_service_client.media.video_streamer import VideoStreamer
from makeup_service_client.media.makeup_applier import MakeupApplier


app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app, async_mode='threading', always_connect=True)


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="127.0.0.1")
    parse.add_argument('--port', default=5002)
    parse.add_argument('--debug', default=True)
    parse.add_argument('--server_host', default="127.0.0.1")
    parse.add_argument('--server_port', default=5000)
    parse.add_argument('--fps', default=5)
    parse.add_argument('--flip', default=True)

    return parse.parse_args()


def provide_images(client, video_streamer, makeup_applier, fps):
    i = 0

    while True:
        ret, image, meta = video_streamer.get_frame()

        if ret:
            package = {
                'id': i,
                'image': image,
                'meta': meta
            }

            client.send_image(package)
            makeup_applier.put_image(package)
            i += 1

        if cv2.waitKey(1) == 27:
            makeup_applier.stop()
            break

        time.sleep(1.0 / fps)


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port
    debug = args.debug
    server_host = args.server_host
    server_port = args.server_port
    flip = args.flip
    fps = args.fps

    frame_size = (512, 512)

    client = MakeupServiceClient(server_host, server_port)
    video_streamer = VideoStreamer(0, frame_size, flip)
    makeup_applier = MakeupApplier()

    socketio.start_background_task(makeup_applier.run)
    socketio.start_background_task(provide_images, client, video_streamer, makeup_applier, fps)

    socketio.run(app, host, port, debug=debug)
