import cv2


class VideoStreamer:
    def __init__(self, source):
        self.__video = cv2.VideoCapture(source)

    def __del__(self):
        self.__video.release()

    def get_frame(self):
        ret, frame = self.__video.read()
        return ret, frame
