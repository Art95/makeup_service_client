from flask import Flask
import os
import argparse
from multiprocessing import Process, JoinableQueue
import time
from flask_socketio import SocketIO
from client.video_streamer import VideoStreamer
from client.makeup_service_client import MakeupServiceClient
from client.makeup_applier import MakeupApplier


app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

socketio.on_event('segmentation', MakeupServiceClient.receive_segmentation)


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="127.0.0.1")
    parse.add_argument('--port', default=5000)
    parse.add_argument('--debug', default=True)

    return parse.parse_args()


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port
    debug = args.debug

    que = JoinableQueue()
    fps = 10
    streamer = VideoStreamer(que, fps=fps)
    makeup_applier = MakeupApplier(que, fps=fps)

    streamer_process = Process(target=streamer.run, daemon=True)
    streamer_process.start()

    time.sleep(5)

    makeup_process = Process(target=makeup_applier.run, daemon=True)
    makeup_process.start()

    que.join()

    print("ended")

    streamer.close()
    makeup_applier.close()

    #socketio.run(app, host, port, debug=debug)