import cv2


class VideoStreamer:
    def __init__(self):
        self.__video = cv2.VideoCapture(0)

    def __del__(self):
        self.__video.release()

    def get_frame(self):
        ret, frame = self.__video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
