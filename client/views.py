import time
import base64
import numpy as np
from client.video_shower import show_frame


def receive_segmentation(data):
    decoded = base64.b64decode(data['segmentation'])
    np_arr = np.frombuffer(decoded, np.uint8)
    show_frame(np_arr)


def send_frames(client, video_streamer):
    while True:
        ret, image = video_streamer.get_frame()

        if ret:
            client.send_image(image)

        time.sleep(0.1)

