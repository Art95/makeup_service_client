import time


def send_frames(client, video_streamer):
    while True:
        ret, image = video_streamer.get_frame()

        if ret:
            client.send_image(image)

        time.sleep(0.1)

