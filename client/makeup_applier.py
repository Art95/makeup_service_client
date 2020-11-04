import cv2
import time
from client.makeup_service_client import MakeupServiceClient


class MakeupApplier:
    def __init__(self, queue, fps=1):
        self.__queue = queue
        self.__stop = False
        self.__fps = fps
        self.__makeup_client = MakeupServiceClient("127.0.0.1")

    def run(self):
        while not self.__stop:
            image = self.__queue.get()
            image = self.apply_makeup(image)

            #cv2.imshow('Makeup', image)
            self.__makeup_client.send_image(image)

            cv2.waitKey(1000 // self.__fps)
            time.sleep(0.2)

            self.__queue.task_done()

    def apply_makeup(self, image):
        return image

    def close(self):
        self.__stop = True
