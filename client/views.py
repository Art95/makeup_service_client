from flask import render_template, Response
from client.video_streamer import VideoStreamer


def index():
    return render_template('index.html')


def video_feed():
    return Response(gen(VideoStreamer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def receive_segmentation(data):
    print(data)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')