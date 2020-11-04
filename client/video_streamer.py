import time
import cv2


class VideoStreamer:
    def __init__(self, queue, flip=True, fps=10):
        self.__flip = flip
        self.__stop = False
        self.__queue = queue
        self.__fps = fps

    def run(self):
        for i in range(50):
        #while not self.__stop:
            stream = cv2.VideoCapture(0)
            ret, image = stream.read()
            stream.release()

            if not ret:
                continue

            if self.__flip:
                image = cv2.flip(image, 1)

            self.__queue.put(image)
            time.sleep(1.0 / self.__fps)

        self.close()

    def close(self):
        self.__stop = True

